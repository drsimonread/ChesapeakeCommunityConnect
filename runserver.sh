#!/usr/bin/env bash
# Start the Django development server using the environment created by setup.sh.
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$ROOT_DIR/cccSite"
VENV_PYTHON="$SITE_DIR/.venv/bin/python"

if [[ ! -f "$SITE_DIR/manage.py" ]]; then
    printf 'Missing project files. Keep runserver.sh in the repository root.\n' >&2
    exit 1
fi
if [[ ! -x "$VENV_PYTHON" ]]; then
    printf 'Virtual environment not found. Run bash setup.sh first.\n' >&2
    exit 1
fi

cd -- "$SITE_DIR"
printf 'Starting the development server on port 8080. Press Ctrl+C to stop.\n'
exec "$VENV_PYTHON" manage.py runserver 8080
