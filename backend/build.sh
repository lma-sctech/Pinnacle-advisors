#!/usr/bin/env bash
# Build script for Render.com deployment
# This script runs during Render build phase

set -o errexit  # Exit on error
set -o pipefail # Exit on pipe failure
set -o nounset  # Exit on undefined variable

echo "========================================="
echo "Starting Pinnacle Advisors Build Process"
echo "========================================="

# Navigate to backend directory
cd backend

echo ""
echo "[1/5] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn whitenoise dj-database-url psycopg2-binary

echo ""
echo "[2/5] Collecting static files..."
python manage.py collectstatic --no-input --clear

echo ""
echo "[3/5] Running database migrations..."
python manage.py migrate --no-input

echo ""
echo "[4/5] Creating cache table (if needed)..."
python manage.py createcachetable || echo "Cache table already exists or not needed"

echo ""
echo "[5/6] Build verification..."
python manage.py check --deploy

echo ""
echo "[6/6] Setup production (superuser + data)..."
python setup_production.py

echo ""
echo "========================================="
echo "Build completed successfully!"
echo "========================================="
