"""
WSGI wrapper for Render deployment.
This allows Render to start the FastAPI app from the root directory.
"""
import sys
import os

# Debug info
print(f"Current directory: {os.getcwd()}")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Backend directory exists: {os.path.exists('backend')}")

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
print(f"Added to sys.path: {backend_path}")

# Import the FastAPI app
try:
    from main import app
    print("✓ Successfully imported FastAPI app")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print(f"sys.path[0]: {sys.path[0]}")
    raise

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting FastAPI server on 0.0.0.0:{port}...")
    uvicorn.run(app, host='0.0.0.0', port=port)
