#!/usr/bin/env bash
# First-time development setup for the Ubuntu/Debian VM in CCCSetupInstructions.md.
set -euo pipefail

usage() {
    cat <<'EOF'
Usage: bash setup.sh [--skip-system-packages] [--runserver]

Install required system packages, create/reuse cccSite/.venv, install Python
requirements, and apply the existing Django migrations to the SQLite database.
Create cccSite/.env from .env.example if it does not already exist.

  --skip-system-packages  Skip apt (prerequisites must already be installed).
  --runserver             Start the development server on port 8080 after setup.
  -h, --help              Show this help without changing anything.

Run from an existing clone as your normal user. Only apt commands use sudo.
Optional MariaDB/PostgreSQL setup is not included.
EOF
}

SKIP_SYSTEM_PACKAGES=false
RUNSERVER=false
for arg in "$@"; do
    case "$arg" in
        --skip-system-packages) SKIP_SYSTEM_PACKAGES=true ;;
        --runserver) RUNSERVER=true ;;
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
    cp -- "$SITE_DIR/.env.example" "$SITE_DIR/.env"
fi

if [[ "$SKIP_SYSTEM_PACKAGES" == false ]]; then
    if ! command -v apt-get >/dev/null 2>&1; then
        printf 'System package installation requires Ubuntu/Debian (apt-get).\nInstall prerequisites manually, then rerun with --skip-system-packages.\n' >&2
        exit 1
    fi

    SUDO=()
    if (( EUID != 0 )); then
        if ! command -v sudo >/dev/null 2>&1; then
            printf 'sudo is required to install system packages. Ask your administrator to install the prerequisites, then use --skip-system-packages.\n' >&2
            exit 1
        fi
        SUDO=(sudo)
    fi

    printf '\nInstalling system packages...\n'
    "${SUDO[@]}" apt-get update
    "${SUDO[@]}" apt-get install -y git python3 python3-venv python3-pip libmagic1 libapache2-mod-wsgi-py3
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

printf '\nApplying database migrations...\n'
cd -- "$SITE_DIR"
"$VENV_PYTHON" manage.py migrate --noinput

printf '\nSetup complete. To start the site in a new terminal:\n'
printf '  cd %q\n  source .venv/bin/activate\n  python manage.py runserver 8080\n' "$SITE_DIR"
printf '\nOpen http://127.0.0.1:8080/ after starting the server.\n'

if [[ "$RUNSERVER" == true ]]; then
    printf '\nStarting the development server. Press Ctrl+C to stop.\n'
    exec "$VENV_PYTHON" manage.py runserver 8080
fi
