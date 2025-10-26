#!/usr/bin/env python3
"""
Minimal API test to verify Railway deployment works
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def test_minimal_imports():
    """Test that all minimal imports work"""
    try:
        print("🧪 Testing minimal imports...")
        
        # Test Google AI
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
        
        # Test FastAPI
        from fastapi import FastAPI
        print("✅ FastAPI imported successfully")
        
        # Test other core dependencies
        import requests
        print("✅ Requests imported successfully")
        
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
        
        from dotenv import load_dotenv
        print("✅ Python-dotenv imported successfully")
        
        from loguru import logger
        print("✅ Loguru imported successfully")
        
        import yaml
        print("✅ PyYAML imported successfully")
        
        print("\n🎊 ALL MINIMAL IMPORTS SUCCESSFUL!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_api_creation():
    """Test that we can create a basic FastAPI app"""
    try:
        print("\n🧪 Testing FastAPI app creation...")
        
        from fastapi import FastAPI
        from pydantic import BaseModel
        
        app = FastAPI(title="AI Arbitrage API", version="1.0.0")
        
        @app.get("/health")
        async def health_check():
            return {"status": "healthy", "message": "AI Arbitrage API is running"}
        
        @app.get("/")
        async def root():
            return {"message": "AI Arbitrage System - Railway Deployed"}
        
        print("✅ FastAPI app created successfully")
        print("✅ Health endpoint configured")
        print("✅ Root endpoint configured")
        
        return True
        
    except Exception as e:
        print(f"❌ FastAPI creation error: {e}")
        return False

def test_google_ai():
    """Test Google AI initialization"""
    try:
        print("\n🧪 Testing Google AI initialization...")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("⚠️  GOOGLE_API_KEY not found in environment")
            return False
        
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Test model initialization
        model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ Google Gemini model initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Google AI error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MINIMAL API TEST FOR RAILWAY DEPLOYMENT")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_minimal_imports,
        test_api_creation,
        test_google_ai
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎊 ALL TESTS PASSED! Railway deployment should work!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)
