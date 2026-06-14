#!/bin/bash
set -e

echo "==> Installing Python 3.12..."
apt-get update
apt-get install -y python3.12 python3.12-venv python3.12-dev

echo "==> Creating virtual environment with Python 3.12..."
python3.12 -m venv /opt/venv
source /opt/venv/bin/activate

echo "==> Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Build complete!"
