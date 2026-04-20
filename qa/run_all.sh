#!/usr/bin/env bash
set -euo pipefail

PORT=8080
BASE_URL="http://127.0.0.1:${PORT}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QA_DIR="${ROOT_DIR}/qa"
SITE_DIR="${ROOT_DIR}/cccSite"

VENV_DIR="${QA_DIR}/.venv"
LOG_FILE="${QA_DIR}/server.log"

echo "QA press-play runner"
echo "Repo: ${ROOT_DIR}"
echo "Site: ${SITE_DIR}"
echo "URL:  ${BASE_URL}"
echo

# Sanity checks
if [ ! -f "${SITE_DIR}/manage.py" ]; then
  echo "ERROR: manage.py not found at ${SITE_DIR}/manage.py"
  exit 1
fi

if [ ! -f "${SITE_DIR}/requirements.txt" ]; then
  echo "ERROR: requirements.txt not found at ${SITE_DIR}/requirements.txt"
  exit 1
fi

echo "[1/6] Creating/activating QA virtualenv..."
if [ ! -d "${VENV_DIR}" ]; then
  python3.10 -m venv "${VENV_DIR}"
fi
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

echo "[2/6] Installing project dependencies (clean)..."
python -m pip install --upgrade pip >/dev/null
pip install -r "${SITE_DIR}/requirements.txt" >/dev/null

echo "[3/6] Installing QA dependencies..."
pip install -r "${QA_DIR}/requirements.txt" >/dev/null

echo "[4/6] Running Django migrations..."
cd "${SITE_DIR}"
python manage.py migrate >/dev/null

echo "[5/6] Starting Django server..."
: > "${LOG_FILE}"
python manage.py runserver "${PORT}" > "${LOG_FILE}" 2>&1 &
SERVER_PID=$!

cleanup() {
  echo
  echo "Stopping server (PID ${SERVER_PID})..."
  kill "${SERVER_PID}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

echo "Waiting for server to respond..."
python - <<PY
import time, sys, requests
url = "${BASE_URL}/"
for _ in range(60):  # ~15 seconds
    try:
        r = requests.get(url, timeout=1)
        if r.status_code < 500:
            print("Server is up.")
            sys.exit(0)
    except Exception:
        pass
    time.sleep(0.25)
print("ERROR: Server did not start in time.")
print("Check log:", "${LOG_FILE}")
sys.exit(1)
PY

echo "[6/6] Running tests..."
cd "${ROOT_DIR}"
QA_BASE_URL="${BASE_URL}" pytest -q qa/ui
echo "PASS"
