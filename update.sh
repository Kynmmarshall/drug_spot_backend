#!/bin/bash
set -e

APP_DIR="$HOME/drug_spot_backend"
REPO="https://github.com/Kynmmarshall/drug_spot_backend.git"
BRANCH="Deployment"
VENV="$APP_DIR/venv/bin"

echo "=== Drug Spot Backend — Deploy ==="
echo "Branch: $BRANCH"
echo ""

if [ ! -d "$APP_DIR/.git" ]; then
    echo "[0] Cloning repo..."
    git clone -b "$BRANCH" "$REPO" "$APP_DIR"
fi

cd "$APP_DIR"

git remote set-url origin "$REPO"

echo "[1/7] Fetching latest changes..."
git fetch origin

echo "[2/7] Checking out $BRANCH..."
git checkout "$BRANCH"
git reset --hard "origin/$BRANCH"

if [ ! -f "$VENV/pip" ]; then
    echo "[2.5] Creating virtual environment..."
    python3 -m venv "$APP_DIR/venv"
fi

echo "[3/7] Installing dependencies..."
"$VENV/pip" install -r requirements.txt --quiet

echo "[4/7] Making migrations..."
"$VENV/python" manage.py makemigrations --noinput

echo "[5/7] Running migrations..."
"$VENV/python" manage.py migrate --noinput

echo "[6/7] Collecting static files..."
"$VENV/python" manage.py collectstatic --noinput --clear

echo "[7/7] Restarting server..."
sudo systemctl restart drugspot

echo ""
echo "=== Deploy complete ==="
sudo systemctl status drugspot --no-pager -l
