#!/usr/bin/env python3
"""Provision the local development MariaDB instance; invoked by setup.sh."""
import fcntl
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys

import MySQLdb
from dotenv import dotenv_values
from dotenv.parser import parse_stream

KEYS = ("MARIADB_HOST", "MARIADB_PORT", "MARIADB_NAME", "MARIADB_USER", "MARIADB_PASSWORD")
DEFAULTS = {"MARIADB_HOST": "127.0.0.1", "MARIADB_PORT": "3306",
            "MARIADB_NAME": "chesapeakeconnect", "MARIADB_USER": "cccapp"}


def fail(message):
    raise SystemExit(message)


def admin(sql, *, contains_password=False):
    command = ([] if os.geteuid() == 0 else ["sudo"]) + [
        "mariadb", "--no-defaults", "--host=localhost", "--protocol=socket", "--user=root", "--binary-mode",
        "--batch", "--skip-column-names"]
    try:
        return subprocess.run(
            command,
            input=sql,
            text=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if contains_password else None,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        fail("MariaDB administration failed. Check the local service and root socket access.")


def sql_string(value):
    # Every admin session uses NO_BACKSLASH_ESCAPES.
    return "'" + value.replace("'", "''") + "'"


def login(config, database=None):
    args = dict(host=config["MARIADB_HOST"], port=int(config["MARIADB_PORT"]),
                user=config["MARIADB_USER"], passwd=config["MARIADB_PASSWORD"],
                connect_timeout=5)
    if database:
        args["db"] = database
    try:
        connection = MySQLdb.connect(**args)
        connection.close()
    except MySQLdb.Error as exc:
        fail(f"MariaDB application login failed ({exc.args[0]}). Credentials were not changed; check the local account and .env before retrying.")


def main():
    path = Path(sys.argv[1])
    # Lock the actual file for the whole operation, including database changes.
    flags = os.O_RDWR | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "r+", encoding="utf-8") as env:
        fcntl.flock(env, fcntl.LOCK_EX)
        os.fchmod(env.fileno(), 0o600)
        entries = list(parse_stream(env))
        seen = set()
        for entry in entries:
            if entry.error:
                fail("Cannot safely parse .env; fix the invalid line before provisioning.")
            if entry.key in KEYS:
                if entry.key in seen:
                    fail(f"Duplicate {entry.key} in .env; resolve it before provisioning.")
                seen.add(entry.key)
        env.seek(0)
        values = dotenv_values(stream=env, interpolate=False)
        config = {}
        for key in KEYS:
            file_value = values.get(key)
            ambient = os.environ.get(key)
            if key in values and (file_value is None or not file_value.strip()):
                fail(f"{key} is empty in .env; set it or remove the entry before provisioning.")
            if ambient is not None and (not ambient.strip() or (file_value is not None and ambient != file_value)):
                fail(f"{key} in the environment conflicts with .env or is empty; resolve it before provisioning.")
            config[key] = file_value if file_value is not None else ambient or DEFAULTS.get(key)
            if config[key] and '${' in config[key]:
                fail(f"{key} contains dotenv interpolation; use a literal value before provisioning.")
        if config["MARIADB_HOST"] != "127.0.0.1" or config["MARIADB_PORT"] != "3306":
            fail("Provisioning only supports 127.0.0.1:3306. Existing MariaDB configuration was left unchanged.")
        for key, limit in (("MARIADB_NAME", 64), ("MARIADB_USER", 32)):
            if not re.fullmatch(r"[A-Za-z0-9_]+", config[key]) or len(config[key]) > limit:
                fail(f"{key} must use ASCII letters, digits, or underscores and be at most {limit} characters.")
        if config["MARIADB_NAME"].lower() in ("mysql", "sys", "information_schema", "performance_schema"):
            fail("Refusing to provision a system database.")
        if config["MARIADB_USER"].lower() in ("root", "mariadb.sys", "mysql"):
            fail("Refusing to provision a system database account.")
        if config["MARIADB_PASSWORD"] and any(c in config["MARIADB_PASSWORD"] for c in "\x00\r\n"):
            fail("MARIADB_PASSWORD cannot contain NUL or line breaks.")

        prefix = "SET SESSION sql_mode='NO_BACKSLASH_ESCAPES';\n"
        user = sql_string(config["MARIADB_USER"])
        account = user + "@'127.0.0.1'"
        exists = admin(prefix + f"SELECT COUNT(*) FROM mysql.user WHERE User={user} AND Host='127.0.0.1';\n") == "1"
        if exists:
            if not config["MARIADB_PASSWORD"]:
                fail("The local MariaDB user already exists but no password is configured. Set its existing password in .env and retry.")
            login(config)
        else:
            config["MARIADB_PASSWORD"] = config["MARIADB_PASSWORD"] or secrets.token_urlsafe(32)

        name = config["MARIADB_NAME"]
        charset = admin(prefix + f"SELECT DEFAULT_CHARACTER_SET_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME={sql_string(name)};\n")
        if charset and charset.lower() != "utf8mb4":
            fail(f"Existing database {name} is not utf8mb4; it was left unchanged.")

        # Persist before creating the user, so a failed or interrupted run can retry.
        env.seek(0)
        content = env.read()
        env.seek(0, os.SEEK_END)
        if content and not content.endswith("\n"):
            env.write("\n")
        for key in KEYS:
            if key not in values:
                value = config[key].replace("\\", "\\\\").replace("'", "\\'")
                env.write(f"{key}='{value}'\n")
        env.flush()
        os.fsync(env.fileno())

        admin(prefix + f"CREATE DATABASE IF NOT EXISTS `{name}` CHARACTER SET utf8mb4;\n")
        if not exists:
            admin(
                prefix + f"CREATE USER IF NOT EXISTS {account} IDENTIFIED BY {sql_string(config['MARIADB_PASSWORD'])};\n",
                contains_password=True,
            )
            # A concurrent creator may have won CREATE USER IF NOT EXISTS.
            login(config)
        # GRANT interprets underscores in database names as wildcards.
        grant_name = name.replace("_", r"\_")
        admin(prefix + f"GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, DROP, REFERENCES ON `{grant_name}`.* TO {account};\n")
        login(config, name)
        print(f"Verified MariaDB application login to {name} at 127.0.0.1:3306.")


if __name__ == "__main__":
    main()
