#!/usr/bin/env bash
set -euo pipefail

PORT=8080
BASE_URL="http://127.0.0.1:${PORT}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QA_DIR="${ROOT_DIR}/qa"
SITE_DIR="${ROOT_DIR}/cccSite"

VENV_DIR="${QA_DIR}/.venv"
LOG_FILE="${QA_DIR}/server.log"
DB_FILE="${SITE_DIR}/db.sqlite3"
REPO_STATUS_BEFORE=""
REPO_STATUS_AFTER=""
SERVER_PID=""

capture_repo_state() {
  git -C "${ROOT_DIR}" status --porcelain=v1 --untracked-files=all -- qa cccSite
}

verify_repo_unchanged() {
  if [ -z "${REPO_STATUS_BEFORE}" ] || [ -z "${REPO_STATUS_AFTER}" ]; then
    return 0
  fi

  if ! diff -u "${REPO_STATUS_BEFORE}" "${REPO_STATUS_AFTER}" >/dev/null; then
    echo "ERROR: QA runner changed tracked or untracked files in qa/ or cccSite/."
    echo "Diff:"
    diff -u "${REPO_STATUS_BEFORE}" "${REPO_STATUS_AFTER}" || true
    return 1
  fi
}

cleanup() {
  exit_code=$?

  if [ -n "${SERVER_PID}" ]; then
    echo
    echo "Stopping server (PID ${SERVER_PID})..."
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
  fi

  if [ -n "${REPO_STATUS_BEFORE}" ] && [ -n "${REPO_STATUS_AFTER}" ]; then
    capture_repo_state > "${REPO_STATUS_AFTER}"
    if ! verify_repo_unchanged; then
      exit_code=1
    fi
    rm -f "${REPO_STATUS_BEFORE}" "${REPO_STATUS_AFTER}"
  fi

  exit "${exit_code}"
}

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

if git -C "${ROOT_DIR}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  REPO_STATUS_BEFORE="$(mktemp)"
  REPO_STATUS_AFTER="$(mktemp)"
  capture_repo_state > "${REPO_STATUS_BEFORE}"
fi
trap cleanup EXIT

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
rm -f "${DB_FILE}"
python manage.py migrate >/dev/null

echo "[5/6] Starting Django server..."
: > "${LOG_FILE}"
python manage.py runserver "${PORT}" > "${LOG_FILE}" 2>&1 &
SERVER_PID=$!

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
