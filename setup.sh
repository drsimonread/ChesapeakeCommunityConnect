#!/usr/bin/env bash
# First-time development setup for the Ubuntu/Debian VM in CCCSetupInstructions.md.
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: bash setup.sh [--skip-system-packages] [--install-mariadb]

Install required system packages, create/reuse cccSite/.venv, install Python
requirements, and apply the existing Django migrations to the SQLite database.
Create cccSite/.env from .env.example if it does not already exist.

  --skip-system-packages  Skip apt (prerequisites must already be installed).
  --install-mariadb       Provision a local MariaDB database and application user.
  -h, --help              Show this help without changing anything.

Run from an existing clone as your normal user. MariaDB administration and
service management also use sudo when needed.
EOF
}

SKIP_SYSTEM_PACKAGES=false
INSTALL_MARIADB=false
for arg in "$@"; do
    case "$arg" in
        --skip-system-packages) SKIP_SYSTEM_PACKAGES=true ;;
        --install-mariadb) INSTALL_MARIADB=true ;;
        -h|--help) usage; exit 0 ;;
        *) printf 'Unknown option: %s\n' "$arg" >&2; usage >&2; exit 2 ;;
    esac
done

trap 'printf "Setup failed at line %s. Fix the error above and rerun the script.\n" "$LINENO" >&2' ERR

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$ROOT_DIR/cccSite"
VENV_DIR="$SITE_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"

if [[ ! -f "$SITE_DIR/manage.py" || ! -f "$SITE_DIR/requirements.txt" ]]; then
    printf 'Missing project files. Keep setup.sh in the repository root.\n' >&2
    exit 1
fi

if [[ ! -e "$SITE_DIR/.env" && ! -L "$SITE_DIR/.env" ]]; then
    printf 'Creating %s from .env.example...\n' "$SITE_DIR/.env"
    (umask 077; cp -- "$SITE_DIR/.env.example" "$SITE_DIR/.env")
fi

SUDO=()
if (( EUID != 0 )) && { [[ "$SKIP_SYSTEM_PACKAGES" == false ]] || [[ "$INSTALL_MARIADB" == true ]]; }; then
    if ! command -v sudo >/dev/null 2>&1; then
        printf 'sudo is required for system package installation or MariaDB administration.\n' >&2
        exit 1
    fi
    SUDO=(sudo)
fi

# Checked before apt-get, which enables and starts a newly installed mariadb-server.
MARIADB_WAS_ENABLED=false
MARIADB_WAS_ACTIVE=false
if [[ "$INSTALL_MARIADB" == true ]]; then
    mariadb_is_starting_or_running() {
        local state
        state=$(systemctl show --property=ActiveState --value mariadb 2>/dev/null) || return 1
        [[ "$state" == active || "$state" == activating || "$state" == reloading ]]
    }

    if systemctl is-enabled --quiet mariadb 2>/dev/null; then
        MARIADB_WAS_ENABLED=true
    fi
    if mariadb_is_starting_or_running; then
        MARIADB_WAS_ACTIVE=true
    fi

    restore_mariadb_state() {
        local failed=false
        if [[ "$MARIADB_WAS_ENABLED" == true ]]; then
            if ! systemctl is-enabled --quiet mariadb 2>/dev/null && ! "${SUDO[@]}" systemctl enable --quiet mariadb; then
                printf 'Failed to restore MariaDB boot enablement.\n' >&2
                failed=true
            fi
        elif systemctl is-enabled --quiet mariadb 2>/dev/null && ! "${SUDO[@]}" systemctl disable --quiet mariadb; then
            printf 'Failed to restore MariaDB boot enablement.\n' >&2
            failed=true
        fi

        if [[ "$MARIADB_WAS_ACTIVE" == true ]]; then
            if ! mariadb_is_starting_or_running && ! "${SUDO[@]}" systemctl start mariadb; then
                printf 'Failed to restore MariaDB service state.\n' >&2
                failed=true
            fi
        elif mariadb_is_starting_or_running; then
            printf 'Stopping MariaDB...\n'
            if ! "${SUDO[@]}" systemctl stop mariadb; then
                printf 'Failed to restore MariaDB service state.\n' >&2
                failed=true
            fi
        fi
        [[ "$failed" == false ]]
    }

    MARIADB_CLEANUP_PENDING=true
    cleanup_mariadb() {
        local status=$?
        trap - EXIT
        trap '' INT TERM HUP
        if [[ "$MARIADB_CLEANUP_PENDING" == true ]] && ! restore_mariadb_state; then
            if (( status == 0 )); then
                status=1
            fi
        fi
        exit "$status"
    }
    trap cleanup_mariadb EXIT
    trap 'exit 130' INT
    trap 'exit 143' TERM
    trap 'exit 129' HUP
fi

if [[ "$SKIP_SYSTEM_PACKAGES" == false ]]; then
    if ! command -v apt-get >/dev/null 2>&1; then
        printf 'System package installation requires Ubuntu/Debian (apt-get).\nInstall prerequisites manually, then rerun with --skip-system-packages.\n' >&2
        exit 1
    fi

    printf '\nInstalling system packages...\n'
    "${SUDO[@]}" apt-get update
    PACKAGES=(
        git python3 python3-venv python3-pip libmagic1 libapache2-mod-wsgi-py3
        build-essential python3-dev default-libmysqlclient-dev pkg-config
    )
    if [[ "$INSTALL_MARIADB" == true ]]; then
        PACKAGES+=(mariadb-server mariadb-client)
    fi
    "${SUDO[@]}" apt-get install -y "${PACKAGES[@]}"
fi

if ! command -v python3 >/dev/null 2>&1; then
    printf 'Python 3 is required. Install Python 3.10+ and its venv support.\n' >&2
    exit 1
fi

# The pinned Django and Pillow requirements need Python 3.10 or newer.
python3 -c 'import sys; sys.exit("Python 3.10+ is required by the project dependencies." if sys.version_info < (3, 10) else 0)'

if [[ ! -e "$VENV_DIR" ]]; then
    printf '\nCreating virtual environment at %s...\n' "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi
if [[ ! -f "$VENV_DIR/pyvenv.cfg" || ! -x "$VENV_PYTHON" ]]; then
    printf 'The environment at %s is incomplete. Move it aside and rerun setup.\n' "$VENV_DIR" >&2
    exit 1
fi
"$VENV_PYTHON" -c 'import sys; sys.exit("The existing virtual environment requires Python 3.10+. Move it aside and rerun setup." if sys.version_info < (3, 10) else 0)'

printf '\nInstalling Python requirements...\n'
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r "$SITE_DIR/requirements.txt"

if [[ "$INSTALL_MARIADB" == true ]]; then
    printf '\nStarting MariaDB...\n'
    "${SUDO[@]}" systemctl start mariadb
    "$VENV_PYTHON" "$ROOT_DIR/provision_mariadb.py" "$SITE_DIR/.env"
    # Restore the original state before continuing with setup.
    if ! restore_mariadb_state; then
        exit 1
    fi
    MARIADB_CLEANUP_PENDING=false
fi

printf '\nApplying database migrations...\n'
cd -- "$SITE_DIR"
CCCSITE_MODE=development "$VENV_PYTHON" manage.py migrate --noinput

printf '\nSetup complete. Run bash runserver.sh from the repository root to start the site.\n'

if [[ "$INSTALL_MARIADB" == true ]]; then
    printf 'Set CCCSITE_MODE=production in cccSite/.env to use MariaDB.\n'
fi

printf 'Open http://127.0.0.1:8080/ after starting the server.\n'
