#!/usr/bin/env python3
"""
Railway Deployment Script for AI Arbitrage Backend
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 Deploying AI Arbitrage Backend to Railway...")
    
    # Check if Railway CLI is installed
    try:
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        print(f"✅ Railway CLI found: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Railway CLI not found. Installing...")
        subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
    
    # Login to Railway (interactive)
    print("\n🔐 Please login to Railway...")
    print("This will open a browser window for authentication.")
    subprocess.run(['railway', 'login'], check=True)
    
    # Initialize Railway project
    print("\n📦 Initializing Railway project...")
    subprocess.run(['railway', 'init'], check=True)
    
    # Set environment variables
    print("\n🔧 Setting environment variables...")
    env_vars = {
        'GOOGLE_API_KEY': 'AIzaSyBOXCq6SjXVOJg7ulD4CT8FoMEvf-wq2ng',
        'AI_PROVIDER': 'google',
        'AI_MODEL': 'gemini-2.5-flash',
        'DATABASE_URL': 'sqlite:///arbitrage.db',
        'PORT': '8000',
        'HOST': '0.0.0.0'
    }
    
    for key, value in env_vars.items():
        subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
        print(f"  ✅ Set {key}")
    
    # Deploy to Railway
    print("\n🚀 Deploying to Railway...")
    subprocess.run(['railway', 'up'], check=True)
    
    # Get the deployment URL
    print("\n🌐 Getting deployment URL...")
    result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
    if result.returncode == 0:
        url = result.stdout.strip()
        print(f"✅ Backend deployed to: {url}")
        
        # Update frontend configuration
        update_frontend_config(url)
        
        print(f"\n🎊 DEPLOYMENT COMPLETE!")
        print(f"Backend URL: {url}")
        print(f"Frontend URL: http://localhost:3001")
        print(f"Full Stack: ✅ LIVE")
        
    else:
        print("❌ Failed to get deployment URL")

def update_frontend_config(backend_url):
    """Update frontend to use live backend URL"""
    frontend_file = Path("frontend/out/index.html")
    
    if frontend_file.exists():
        content = frontend_file.read_text()
        # Update API URL in the frontend
        updated_content = content.replace(
            'const API_URL = process.env.NEXT_PUBLIC_API_URL || \'http://localhost:8000\';',
            f'const API_URL = \'{backend_url}\';'
        )
        frontend_file.write_text(updated_content)
        print(f"✅ Updated frontend to use backend: {backend_url}")

if __name__ == "__main__":
    main()
