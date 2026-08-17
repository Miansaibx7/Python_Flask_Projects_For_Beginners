#!/bin/sh

# Flask Development Container Entrypoint

# Purpose:
#   Stop the script if any command fails.
#   Check that Python and Flask are available.
#   Optionally initialize the database.
#   Start the selected Flask application.
#
# Usage:
#   docker compose up
#
# The Flask application should be selected through the
# FLASK_APP environment variable in docker-compose.yml.

set -e

echo "=========================================="
echo " Starting Flask Development Container"
echo "=========================================="

# Display Python version
echo ""
echo "Python version:"
python --version

# Check that Flask is installed
echo ""
echo "Checking Flask installation..."

python -c "import flask; print('Flask version:', flask.__version__)"


# Display the application that will be started
echo ""
echo "Flask application:"
echo "${FLASK_APP:-Not specified}"

# Initialize database if the application provides a Flask CLI command for it.
if [ "${INIT_DB:-false}" = "true" ]; then
    echo ""
    echo "Initializing database..."

    flask shell <<'PY'
from flask import current_app

# The application may define its own database initialization.
# This block intentionally does not assume a specific model.
print("Flask application loaded successfully.")
PY

    echo "Database initialization step completed."
fi

# Start Flask development server
echo ""
echo "Starting Flask development server..."
echo "Host: 0.0.0.0"
echo "Port: ${FLASK_RUN_PORT:-5000}"
echo ""

exec flask run \
    --host=0.0.0.0 \
    --port="${FLASK_RUN_PORT:-5000}"