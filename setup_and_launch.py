#!/usr/bin/env python3
"""
Interactive Setup & Launch Script
Helps you configure API keys and start the system
"""

import os
import sys
from pathlib import Path

def print_header():
    print("\n" + "="*70)
    print("  🚀 AI ARBITRAGE SYSTEM - INTERACTIVE SETUP & LAUNCH")
    print("="*70 + "\n")

def check_env_file():
    """Check if .env file exists"""
    env_file = Path('.env')
    return env_file.exists()

def get_api_key_choice():
    """Ask user which API they want to use"""
    print("Which AI service do you want to use?\n")
    print("1. OpenAI (GPT-4) - Recommended")
    print("   • Most powerful reasoning")
    print("   • Cost: ~$20-50/month depending on usage")
    print("   • Sign up: https://platform.openai.com\n")
    
    print("2. Anthropic (Claude) - Alternative")
    print("   • Excellent reasoning, different style")
    print("   • Cost: Similar to OpenAI")
    print("   • Sign up: https://console.anthropic.com\n")
    
    print("3. I'll add the key manually later\n")
    
    choice = input("Enter choice (1-3): ").strip()
    return choice

def prompt_for_key(service_name, key_prefix):
    """Prompt user to enter API key"""
    print(f"\n📝 Enter your {service_name} API key:")
    print(f"   (It should start with '{key_prefix}')")
    print(f"   Or press Enter to skip and add later\n")
    
    key = input("API Key: ").strip()
    
    if key and len(key) > 20:
        return key
    else:
        print(f"   ⚠️  No key entered - you can add it to .env file later")
        return None

def update_env_file(api_key, service):
    """Update .env file with API key"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("   ❌ .env file not found!")
        return False
    
    # Read current content
    with open(env_path, 'r') as f:
        content = f.read()
    
    # Update the appropriate key
    if service == 'openai':
        content = content.replace(
            'OPENAI_API_KEY=sk-proj-ADD_YOUR_KEY_HERE',
            f'OPENAI_API_KEY={api_key}'
        )
    else:  # anthropic
        content = content.replace(
            '# ANTHROPIC_API_KEY=sk-ant-ADD_YOUR_KEY_HERE',
            f'ANTHROPIC_API_KEY={api_key}'
        )
        content = content.replace(
            'AI_MODEL=gpt-4-turbo-preview',
            'AI_MODEL=claude-3-opus-20240229'
        )
    
    # Write back
    with open(env_path, 'w') as f:
        f.write(content)
    
    print(f"   ✅ API key saved to .env file!")
    return True

def check_docker():
    """Check if Docker is installed"""
    import subprocess
    
    try:
        result = subprocess.run(
            ['docker', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ Docker found: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("   ⚠️  Docker not found")
    return False

def check_docker_compose():
    """Check if Docker Compose is installed"""
    import subprocess
    
    try:
        result = subprocess.run(
            ['docker-compose', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ Docker Compose found: {result.stdout.strip()}")
            return True
    except:
        pass
    
    try:
        result = subprocess.run(
            ['docker', 'compose', 'version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ Docker Compose found: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("   ⚠️  Docker Compose not found")
    return False

def main():
    print_header()
    
    # Check environment
    if not check_env_file():
        print("❌ .env file not found! Creating one...")
        print("   Please run this script again after .env is created.")
        return
    
    # API Key setup
    print("STEP 1: Configure AI API Key")
    print("-" * 70)
    
    choice = get_api_key_choice()
    
    api_key = None
    service = None
    
    if choice == '1':
        api_key = prompt_for_key("OpenAI", "sk-proj-")
        service = 'openai'
    elif choice == '2':
        api_key = prompt_for_key("Anthropic Claude", "sk-ant-")
        service = 'anthropic'
    else:
        print("\n   ℹ️  Skipping API key setup")
        print("   You can add your key manually to the .env file")
    
    if api_key and service:
        update_env_file(api_key, service)
    
    # Check Docker
    print("\n\nSTEP 2: Check Docker Installation")
    print("-" * 70)
    
    has_docker = check_docker()
    has_compose = check_docker_compose() if has_docker else False
    
    # Launch options
    print("\n\nSTEP 3: Choose Launch Mode")
    print("-" * 70)
    print("\nHow do you want to run the system?\n")
    
    print("1. 🐍 Python Backend Only (Simple)")
    print("   • Just the AI engine and scrapers")
    print("   • No dashboard, terminal output only")
    print("   • Lowest resource usage")
    print("   • Perfect for testing\n")
    
    if has_docker and has_compose:
        print("2. 🎨 Full Stack with Dashboard (Recommended)")
        print("   • Beautiful React dashboard")
        print("   • Real-time charts and graphs")
        print("   • All services (Python + NestJS + Frontend)")
        print("   • Requires Docker\n")
    else:
        print("2. 🎨 Full Stack with Dashboard (Docker required)")
        print("   • ⚠️  Docker not found - install Docker Desktop first")
        print("   • Download: https://www.docker.com/products/docker-desktop\n")
    
    print("3. 📊 Just run Demo again")
    print("   • See the system in action")
    print("   • No API key needed\n")
    
    launch_choice = input("Enter choice (1-3): ").strip()
    
    print("\n" + "="*70)
    
    if launch_choice == '1':
        print("\n🚀 Launching Python Backend...\n")
        print("The system will:")
        print("  • Scan marketplaces every 10 minutes")
        print("  • Analyze opportunities with AI")
        print("  • Save profitable deals to database")
        print("  • Wait for your approval to purchase\n")
        
        if not api_key:
            print("⚠️  WARNING: No API key configured!")
            print("   The system will use demo mode without real scanning.\n")
            proceed = input("Continue anyway? (y/n): ").lower()
            if proceed != 'y':
                print("\nℹ️  Setup cancelled. Add your API key to .env and run again.")
                return
        
        print("\nStarting in 3 seconds... (Press Ctrl+C to cancel)\n")
        import time
        try:
            for i in range(3, 0, -1):
                print(f"   {i}...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            return
        
        print("\n" + "="*70)
        print("🚀 LAUNCHING AI ARBITRAGE SYSTEM")
        print("="*70 + "\n")
        
        os.system("source venv/bin/activate && python main.py")
    
    elif launch_choice == '2':
        if not has_docker or not has_compose:
            print("\n❌ Docker or Docker Compose not found!")
            print("\nTo use the dashboard, install Docker Desktop:")
            print("   https://www.docker.com/products/docker-desktop")
            print("\nThen run this script again or use: docker-compose up -d")
            return
        
        print("\n🎨 Launching Full Stack...\n")
        print("This will start:")
        print("  ✅ Python AI Backend (FastAPI)")
        print("  ✅ NestJS Microservices")
        print("  ✅ React Dashboard")
        print("  ✅ PostgreSQL Database")
        print("  ✅ MongoDB (high-volume storage)")
        print("  ✅ Redis (caching)")
        print("  ✅ Nginx (load balancer)\n")
        
        print("Starting Docker services... (this may take 1-2 minutes)\n")
        
        result = os.system("docker-compose up -d")
        
        if result == 0:
            print("\n" + "="*70)
            print("✅ FULL STACK LAUNCHED SUCCESSFULLY!")
            print("="*70)
            print("\n📊 Access your dashboard at:")
            print("   http://localhost:3000\n")
            print("📚 API Documentation:")
            print("   http://localhost:8000/docs\n")
            print("💡 To view logs:")
            print("   docker-compose logs -f\n")
            print("🛑 To stop:")
            print("   docker-compose down\n")
            print("="*70)
        else:
            print("\n❌ Docker launch failed")
            print("   Check if Docker Desktop is running")
            print("   Or try: python main.py (backend only)")
    
    elif launch_choice == '3':
        print("\n🎬 Running Demo Mode...\n")
        os.system("source venv/bin/activate && python demo_mode.py")
    
    else:
        print("\n❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

