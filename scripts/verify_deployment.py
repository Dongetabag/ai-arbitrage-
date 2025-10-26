#!/usr/bin/env python3
"""
Deployment Verification Script
Run after deployment to verify everything works
"""

import requests
import asyncio
import sys
from typing import Dict, List

class DeploymentVerifier:
    def __init__(self, backend_url: str, frontend_url: str):
        self.backend_url = backend_url
        self.frontend_url = frontend_url
        self.results: List[Dict] = []
    
    def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
            self.results.append({"test": "Backend Health", "status": "✅ PASS"})
        except Exception as e:
            self.results.append({"test": "Backend Health", "status": f"❌ FAIL: {e}"})
    
    def test_backend_docs(self):
        """Test API documentation endpoint"""
        try:
            response = requests.get(f"{self.backend_url}/docs", timeout=10)
            assert response.status_code == 200
            self.results.append({"test": "API Docs", "status": "✅ PASS"})
        except Exception as e:
            self.results.append({"test": "API Docs", "status": f"❌ FAIL: {e}"})
    
    def test_frontend_load(self):
        """Test frontend loading"""
        try:
            response = requests.get(self.frontend_url, timeout=10)
            assert response.status_code == 200
            assert len(response.content) > 1000  # Basic sanity check
            self.results.append({"test": "Frontend Load", "status": "✅ PASS"})
        except Exception as e:
            self.results.append({"test": "Frontend Load", "status": f"❌ FAIL: {e}"})
    
    def test_cors(self):
        """Test CORS configuration"""
        try:
            headers = {"Origin": self.frontend_url}
            response = requests.options(
                f"{self.backend_url}/api/opportunities",
                headers=headers,
                timeout=10
            )
            assert "access-control-allow-origin" in response.headers
            self.results.append({"test": "CORS Configuration", "status": "✅ PASS"})
        except Exception as e:
            self.results.append({"test": "CORS Configuration", "status": f"❌ FAIL: {e}"})
    
    def test_api_endpoint(self):
        """Test actual API endpoint"""
        try:
            response = requests.get(
                f"{self.backend_url}/api/opportunities",
                timeout=10
            )
            assert response.status_code in [200, 401]  # 401 if auth required
            self.results.append({"test": "API Endpoint", "status": "✅ PASS"})
        except Exception as e:
            self.results.append({"test": "API Endpoint", "status": f"❌ FAIL: {e}"})
    
    def run_all_tests(self):
        """Run all verification tests"""
        print("🔍 Running Deployment Verification Tests...\n")
        
        self.test_backend_health()
        self.test_backend_docs()
        self.test_frontend_load()
        self.test_cors()
        self.test_api_endpoint()
        
        print("\n📊 Test Results:")
        print("=" * 50)
        for result in self.results:
            print(f"{result['test']}: {result['status']}")
        print("=" * 50)
        
        # Check if all passed
        failed = [r for r in self.results if "FAIL" in r["status"]]
        if failed:
            print(f"\n❌ {len(failed)} tests failed!")
            sys.exit(1)
        else:
            print("\n✅ All tests passed! Deployment verified.")
            sys.exit(0)

if __name__ == "__main__":
    # Update these with your actual URLs
    BACKEND_URL = "https://web-production-8c988.up.railway.app"
    FRONTEND_URL = "https://frontend-sage-two-68.vercel.app"
    
    verifier = DeploymentVerifier(BACKEND_URL, FRONTEND_URL)
    verifier.run_all_tests()
