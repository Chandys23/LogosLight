#!/bin/bash
set -e

VENV_DIR="/opt/render/project/src/appenv"

echo "==> Creating virtual environment at $VENV_DIR..."
python3 -m venv "$VENV_DIR"

echo "==> Installing dependencies into venv..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

echo "==> Verifying installation..."
"$VENV_DIR/bin/python" -c "import fastapi; print(f'FastAPI {fastapi.__version__} ready')"

echo "==> Build complete!"
