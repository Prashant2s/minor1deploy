#!/usr/bin/env python3
"""
Local development server runner
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables for local development
os.environ.setdefault('DB_URL', 'sqlite:///./university.db')
os.environ.setdefault('UPLOAD_DIR', './uploads')
os.environ.setdefault('LOG_LEVEL', 'DEBUG')

# Import and run the app
from app.main import create_app

if __name__ == "__main__":
    print("Starting University Verifier Backend...")
    print("Database: SQLite (local development)")
    print("Upload Directory: ./uploads")
    print("API will be available at: http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    print("-" * 50)
    
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
