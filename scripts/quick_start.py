"""
Quick Start Script
Interactive setup wizard for the AI Arbitrage System
"""

import os
import sys
from pathlib import Path

def quick_start():
    """Interactive quick start"""
    
    print("\n" + "=" * 70)
    print("  AI ARBITRAGE SYSTEM - QUICK START WIZARD")
    print("=" * 70)
    
    print("\nWelcome! This wizard will help you set up the AI Arbitrage System.")
    print("\nYou'll need:")
    print("  - An OpenAI or Anthropic API key")
    print("  - Amazon Seller account (for selling)")
    print("  - Keepa API key (recommended)")
    print("  - BookScouter API key (free, for books)")
    
    input("\nPress Enter to continue...")
    
    # Check if .env exists
    env_file = Path('.env')
    
    if env_file.exists():
        print("\n⚠️  .env file already exists")
        overwrite = input("Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Exiting...")
            return
    
    # Create .env interactively
    print("\n" + "-" * 70)
    print("STEP 1: AI Configuration")
    print("-" * 70)
    
    ai_provider = input("\nChoose AI provider (openai/anthropic): ").lower()
    
    if ai_provider == 'openai':
        openai_key = input("Enter OpenAI API key: ").strip()
        ai_model = "gpt-4-turbo-preview"
        anthropic_key = ""
    else:
        anthropic_key = input("Enter Anthropic API key: ").strip()
        ai_model = "claude-3-opus-20240229"
        openai_key = ""
    
    print("\n" + "-" * 70)
    print("STEP 2: Core APIs")
    print("-" * 70)
    
    keepa_key = input("\nEnter Keepa API key (press Enter to skip): ").strip()
    bookscouter_key = input("Enter BookScouter API key (press Enter to skip): ").strip()
    
    print("\n" + "-" * 70)
    print("STEP 3: System Limits")
    print("-" * 70)
    
    max_purchase = input("\nMax purchase per item ($): [default: 500] ").strip() or "500"
    max_daily_spend = input("Max daily spend ($): [default: 2000] ").strip() or "2000"
    min_margin = input("Minimum profit margin (%): [default: 20] ").strip() or "20"
    min_margin = float(min_margin) / 100
    
    print("\n" + "-" * 70)
    print("STEP 4: Location")
    print("-" * 70)
    
    zipcode = input("\nYour ZIP code: [default: 02101] ").strip() or "02101"
    
    print("\n" + "-" * 70)
    print("STEP 5: Safety Settings")
    print("-" * 70)
    
    print("\nAuto-purchase allows the system to buy items automatically.")
    print("RECOMMENDED: Start with 'no' and review purchases manually")
    auto_purchase = input("Enable auto-purchase? (yes/no): [default: no] ").strip().lower()
    auto_purchase = "true" if auto_purchase == 'yes' else "false"
    
    # Write .env file
    env_content = f"""# AI Services
OPENAI_API_KEY={openai_key}
ANTHROPIC_API_KEY={anthropic_key}
AI_MODEL={ai_model}

# Database
DATABASE_URL=sqlite:///arbitrage.db
REDIS_URL=redis://localhost:6379/0

# Core APIs
KEEPA_API_KEY={keepa_key}
BOOKSCOUTER_API_KEY={bookscouter_key}

# System Settings
MAX_PURCHASE_AMOUNT={max_purchase}
MAX_DAILY_SPEND={max_daily_spend}
MIN_PROFIT_MARGIN={min_margin}
ZIPCODE={zipcode}

# Automation
AUTO_PURCHASE={auto_purchase}

# Logging
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ .env file created successfully!")
    
    # Initialize database
    print("\n" + "-" * 70)
    print("STEP 6: Initialize Database")
    print("-" * 70)
    
    init_db = input("\nInitialize database now? (y/n): ").lower()
    
    if init_db == 'y':
        print("\nInitializing database...")
        try:
            from database.models import Base
            from sqlalchemy import create_engine
            
            db_url = 'sqlite:///arbitrage.db'
            engine = create_engine(db_url)
            Base.metadata.create_all(engine)
            
            print("✅ Database initialized!")
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("SETUP COMPLETE!")
    print("=" * 70)
    
    print("\n📋 Next Steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Test API connections: python scripts/test_apis.py")
    print("   3. Start the system: python main.py")
    
    print("\n📚 Documentation:")
    print("   - README.md - System overview")
    print("   - USAGE_GUIDE.md - How to use the system")
    print("   - API_SETUP_GUIDE.md - Detailed API setup")
    print("   - DEPLOYMENT.md - Deployment options")
    
    print("\n⚠️  Important:")
    print("   - Start with auto_purchase=false and review manually")
    print("   - Monitor the first 100 opportunities closely")
    print("   - Check logs/arbitrage_*.log for activity")
    
    print("\n💰 Expected Results:")
    print("   - First week: 10-30 opportunities/day")
    print("   - First month: $500-1,500 profit")
    print("   - After optimization: $2,000-5,000/month")
    
    print("\n" + "=" * 70)
    print()


if __name__ == "__main__":
    try:
        quick_start()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)

