#!/usr/bin/env bash
# Start the Django development server using the environment created by setup.sh.
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$ROOT_DIR/cccSite"
VENV_PYTHON="$SITE_DIR/.venv/bin/python"

usage() {
    printf 'Usage: bash runserver.sh [--production | --help]\n'
    printf 'Select the database with CCCSITE_MODE in cccSite/.env.\n'
    printf '  --production  Use MariaDB and start the local service if needed.\n'
    printf '                Stop the service on exit if this run started it.\n'
}

production=false
if (( $# > 1 )); then
    usage >&2
    exit 2
fi
if (( $# == 1 )); then
    case "$1" in
        --production) production=true ;;
        -h|--help) usage; exit 0 ;;
        *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
    esac
fi

if [[ ! -f "$SITE_DIR/manage.py" ]]; then
    printf 'Missing project files. Keep runserver.sh in the repository root.\n' >&2
    exit 1
fi
if [[ ! -x "$VENV_PYTHON" ]]; then
    printf 'Virtual environment not found. Run bash setup.sh first.\n' >&2
    exit 1
fi

started_mariadb=false
django_pid=
service_command=(systemctl)

cleanup() {
    local status=$?
    trap '' INT TERM HUP

    if [[ -n "$django_pid" ]]; then
        # Signal both Django and its autoreloader child.
        kill -TERM -- "-$django_pid" 2>/dev/null || true
        wait "$django_pid" 2>/dev/null || true
    fi

    printf '\nStopping MariaDB...\n'
    if ! "${service_command[@]}" stop mariadb; then
        printf 'Could not stop the MariaDB service.\n' >&2
        if (( status == 0 )); then
            status=1
        fi
    fi
    exit "$status"
}

start_local_mariadb() {
    # Serialize service ownership between launches from this checkout.
    exec {mariadb_lock}< "$ROOT_DIR"
    if ! flock -n "$mariadb_lock"; then
        printf 'Another production launcher is using local MariaDB in this checkout.\n' >&2
        exit 1
    fi

    if systemctl is-active --quiet mariadb; then
        return
    fi

    if (( EUID != 0 )); then
        service_command=(sudo systemctl)
    fi

    started_mariadb=true
    trap cleanup EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    trap 'exit 129' HUP

    printf 'Starting MariaDB...\n'
    "${service_command[@]}" start mariadb
}

cd -- "$SITE_DIR"
if [[ "$production" == true ]]; then
    export CCCSITE_MODE=production
    database_host=$("$VENV_PYTHON" -c 'from cccSite.settings import DATABASES; print(DATABASES["default"]["HOST"])')
    case "$database_host" in
        localhost|127.0.0.1|::1|/*) start_local_mariadb ;;
    esac
fi

printf 'Applying database migrations.\n'
"$VENV_PYTHON" manage.py migrate --noinput
printf 'Starting the development server on port 8080. Press Ctrl+C to stop.\n'

if [[ "$started_mariadb" == true ]]; then
    setsid "$VENV_PYTHON" manage.py runserver 8080 &
    django_pid=$!
    wait "$django_pid"
    exit
fi

exec "$VENV_PYTHON" manage.py runserver 8080
