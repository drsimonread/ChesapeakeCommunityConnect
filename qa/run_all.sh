#!/usr/bin/env bash
set -euo pipefail

PORT=8080
BASE_URL="http://127.0.0.1:${PORT}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
QA_DIR="${ROOT_DIR}/qa"
SITE_DIR="${ROOT_DIR}/cccSite"

VENV_DIR="${QA_DIR}/.venv"
LOG_FILE="${QA_DIR}/server.log"
QA_DB_FILE="${QA_DIR}/qa.sqlite3"

SERVER_PID=""
REPO_STATUS_BEFORE=""
REPO_STATUS_AFTER=""
PYTEST_LOG=""

capture_repo_state() {
  git -C "${ROOT_DIR}" status --short --untracked-files=all
}

cleanup() {
  local exit_code=$?

  if [ -n "${SERVER_PID}" ] && kill -0 "${SERVER_PID}" >/dev/null 2>&1; then
    kill "${SERVER_PID}" >/dev/null 2>&1 || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi

  if [ -n "${PYTEST_LOG}" ] && [ -f "${PYTEST_LOG}" ]; then
    rm -f "${PYTEST_LOG}"
  fi

  if [ -n "${REPO_STATUS_BEFORE}" ] && [ -f "${REPO_STATUS_BEFORE}" ]; then
    capture_repo_state > "${REPO_STATUS_AFTER}"
    if ! cmp -s "${REPO_STATUS_BEFORE}" "${REPO_STATUS_AFTER}"; then
      echo
      echo "WARNING: Repository state changed while qa/run_all.sh was running."
      echo "Review git status before committing."
    fi
    rm -f "${REPO_STATUS_BEFORE}" "${REPO_STATUS_AFTER}"
  fi

  trap - EXIT
  exit "${exit_code}"
}

echo "QA press-play runner"
echo "Repo: ${ROOT_DIR}"
echo "Site: ${SITE_DIR}"
echo "URL:  ${BASE_URL}"
echo "DB:   ${QA_DB_FILE}"
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
rm -f "${QA_DB_FILE}"
CCCSITE_SQLITE_DB="${QA_DB_FILE}" python manage.py migrate >/dev/null

echo "[5/6] Starting Django server..."
: > "${LOG_FILE}"
CCCSITE_SQLITE_DB="${QA_DB_FILE}" python manage.py runserver "${PORT}" > "${LOG_FILE}" 2>&1 &
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
PYTEST_LOG="$(mktemp)"

set +e
QA_BASE_URL="${BASE_URL}" pytest -q qa/ui 2>&1 | tee "${PYTEST_LOG}"
PYTEST_STATUS=${PIPESTATUS[0]}
set -e

read -r TOTAL_TESTS PASSED_TESTS FAILED_TESTS FINAL_RESULT < <(
  python - "${PYTEST_LOG}" "${PYTEST_STATUS}" <<'PY'
import re
import sys

log_path = sys.argv[1]
pytest_status = int(sys.argv[2])

with open(log_path, "r", encoding="utf-8") as handle:
    lines = [line.strip() for line in handle if line.strip()]

summary_line = ""
for line in reversed(lines):
    if re.search(r"\b(?:passed|failed|error|errors|skipped|xfailed|xpassed)\b", line):
        summary_line = line
        break

counts = {
    "passed": 0,
    "failed": 0,
    "error": 0,
    "errors": 0,
    "skipped": 0,
    "xfailed": 0,
    "xpassed": 0,
}

for value, label in re.findall(
    r"(\d+)\s+(passed|failed|error|errors|skipped|xfailed|xpassed)",
    summary_line,
):
    counts[label] += int(value)

passed = counts["passed"]
failed = counts["failed"] + counts["error"] + counts["errors"]
total = passed + failed + counts["skipped"] + counts["xfailed"] + counts["xpassed"]
result = "PASS" if pytest_status == 0 else "FAIL"

print(total, passed, failed, result)
PY
)

echo
echo "Test Summary"
echo "Tests Run: ${TOTAL_TESTS}"
echo "Passed: ${PASSED_TESTS}"
echo "Failed: ${FAILED_TESTS}"
echo "Result: ${FINAL_RESULT}"

if [ "${PYTEST_STATUS}" -ne 0 ]; then
  exit "${PYTEST_STATUS}"
fi
