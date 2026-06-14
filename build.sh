#!/bin/bash
set -e

echo "==> Python version:"
python3 --version

echo "==> Python path:"
which python3

echo "==> Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "==> Verifying fastapi installation..."
python3 -c "import fastapi; print(f'✓ FastAPI {fastapi.__version__} installed')"

echo "==> Build complete!"
