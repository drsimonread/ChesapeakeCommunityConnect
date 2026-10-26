#starts Django website whenever you need it

#!/bin/bash
set -euo pipefail

# Navigate to the directory containing this script
cd "$(dirname "$0")"

echo "Starting Chesapeake Community Connect..."

# Verify virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment missing."
    echo "Please run setup.sh first."
    exit 1
fi

# Activate environment
source .venv/bin/activate

# Apply pending database migrations
python manage.py migrate --noinput

# Start Django
echo "Website starting on port 8080..."

python manage.py runserver 0.0.0.0:8080
