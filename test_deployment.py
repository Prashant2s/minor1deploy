#!/usr/bin/env python3
"""
Test script for deployment readiness
"""
import os
import sys
import requests
import json
from pathlib import Path

def test_backend_imports():
    """Test if backend can be imported successfully"""
    print("Testing backend imports...")
    try:
        from app.main import app
        print("✓ Backend imports successful")
        return True
    except Exception as e:
        print(f"✗ Backend import failed: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\nTesting environment configuration...")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠ No .env file found - using default configuration")
    
    # Test configuration loading
    try:
        from app.core.config import settings
        print(f"✓ Database URL: {settings.DB_URL}")
        print(f"✓ Upload directory: {settings.UPLOAD_DIR}")
        print(f"✓ CORS origin: {settings.CORS_ORIGIN}")
        print(f"✓ Max file size: {settings.MAX_FILE_SIZE}")
        
        if settings.OPENAI_API_KEY:
            print("✓ OpenAI API key configured")
        else:
            print("⚠ OpenAI API key not configured - AI features will be disabled")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\nTesting database connection...")
    try:
        from app.db.session import init_engine, get_engine
        from app.core.config import settings
        from sqlalchemy import text
        
        init_engine(settings.DB_URL)
        engine = get_engine()
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("âœ“ Database connection successful")
            return True
    except Exception as e:
        print(f"âœ— Database connection failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\nTesting API endpoints...")
    
    try:
        from app.main import app
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/v1/health')
            if response.status_code == 200:
                print("✓ Health endpoint working")
                data = response.get_json()
                print(f"  Status: {data.get('status')}")
                print(f"  AI Status: {data.get('ai_status')}")
            else:
                print(f"✗ Health endpoint failed: {response.status_code}")
                return False
            
            # Test CORS headers
            response = client.options('/api/v1/health')
            if 'Access-Control-Allow-Origin' in response.headers:
                print("✓ CORS headers configured")
            else:
                print("⚠ CORS headers not found")
            
            return True
    except Exception as e:
        print(f"✗ API endpoint test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\nTesting file operations...")
    
    try:
        from app.services.images import is_allowed_file, save_and_process_file
        from app.services.ocr import run_ocr
        from app.core.config import settings
        from pathlib import Path
        import io
        
        # Test file validation
        test_files = [
            ("test.pdf", True),
            ("test.jpg", True),
            ("test.png", True),
            ("test.txt", False),
            ("test.exe", False)
        ]
        
        for filename, expected in test_files:
            result = is_allowed_file(filename)
            if result == expected:
                print(f"✓ File validation for {filename}: {result}")
            else:
                print(f"✗ File validation for {filename}: expected {expected}, got {result}")
                return False
        
        # Test upload directory
        upload_dir = Path(settings.UPLOAD_DIR)
        if upload_dir.exists():
            print("✓ Upload directory exists")
        else:
            print("⚠ Upload directory does not exist")
        
        return True
    except Exception as e:
        print(f"✗ File operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing AI Certificate Verifier for Deployment")
    print("=" * 50)
    
    tests = [
        test_backend_imports,
        test_environment_config,
        test_database_connection,
        test_api_endpoints,
        test_file_operations
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready for deployment.")
        return 0
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
