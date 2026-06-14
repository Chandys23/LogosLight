"""
WSGI wrapper for Render deployment.
This allows Render to start the FastAPI app from the root directory.
"""
import sys
import os

# Verify we're in the right directory
print(f"Current directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
print(f"Backend directory exists: {os.path.exists('backend')}")

# Add backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the FastAPI app
from main import app

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting FastAPI server on port {port}...")
    uvicorn.run(app, host='0.0.0.0', port=port)
