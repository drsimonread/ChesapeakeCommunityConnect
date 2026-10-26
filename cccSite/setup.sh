
#!/bin/bash
# Chesapeake Community Connect - Ubuntu setup
set -euo pipefail

cd "$(dirname "$0")"

echo "Starting CCC installation..."

if [ ! -f manage.py ] || [ ! -f requirements.txt ]; then
    echo "ERROR: Run this script from the CCC Django project."
    exit 1
fi

PYTHON="$HOME/.pyenv/versions/3.10.22/bin/python"

if [ ! -x "$PYTHON" ]; then
    echo "ERROR: Python 3.10.22 was not found at $PYTHON"
    exit 1
fi

echo "Installing Ubuntu dependencies..."
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git python3-venv python3-pip \
    libmagic1 libjpeg-dev zlib1g-dev

if [ ! -f .venv/bin/activate ]; then
    echo "Creating Python 3.10 virtual environment..."
    "$PYTHON" -m venv .venv
fi

source .venv/bin/activate

echo "Installing Python packages..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Checking Django..."
python manage.py check

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "CCC INSTALLATION COMPLETE!"
echo "Run ./start.sh to launch the website."
