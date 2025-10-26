"""
API Connection Tester
Tests all configured APIs to ensure they're working
"""

import os
import asyncio
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()


async def test_openai():
    """Test OpenAI API"""
    print("\n🤖 Testing OpenAI API...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("   ❌ OPENAI_API_KEY not set")
        return False
    
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        print(f"   ✅ OpenAI connected successfully")
        return True
    except Exception as e:
        print(f"   ❌ OpenAI error: {e}")
        return False


async def test_keepa():
    """Test Keepa API"""
    print("\n📊 Testing Keepa API...")
    
    api_key = os.getenv('KEEPA_API_KEY')
    if not api_key:
        print("   ⚠️  KEEPA_API_KEY not set (optional but recommended)")
        return False
    
    try:
        import keepa
        api = keepa.Keepa(api_key)
        
        # Test with a known ASIN
        products = api.query('B00X4WHP5E')  # Example ASIN
        
        if products:
            print(f"   ✅ Keepa connected successfully")
            return True
    except Exception as e:
        print(f"   ❌ Keepa error: {e}")
        return False


async def test_bookscouter():
    """Test BookScouter API"""
    print("\n📚 Testing BookScouter API...")
    
    api_key = os.getenv('BOOKSCOUTER_API_KEY')
    if not api_key:
        print("   ⚠️  BOOKSCOUTER_API_KEY not set (recommended for books)")
        return False
    
    try:
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://bookscouter.com/api/v3/prices",
                params={'api_key': api_key, 'isbn': '9780134685991'},
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"   ✅ BookScouter connected successfully")
                return True
            else:
                print(f"   ❌ BookScouter returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"   ❌ BookScouter error: {e}")
        return False


async def test_twilio():
    """Test Twilio API"""
    print("\n📱 Testing Twilio API...")
    
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    
    if not account_sid or not auth_token:
        print("   ⚠️  Twilio credentials not set (optional for SMS)")
        return False
    
    try:
        from twilio.rest import Client
        
        client = Client(account_sid, auth_token)
        account = client.api.accounts(account_sid).fetch()
        
        print(f"   ✅ Twilio connected successfully (Status: {account.status})")
        return True
    except Exception as e:
        print(f"   ❌ Twilio error: {e}")
        return False


async def test_sendgrid():
    """Test SendGrid API"""
    print("\n✉️  Testing SendGrid API...")
    
    api_key = os.getenv('SENDGRID_API_KEY')
    if not api_key:
        print("   ⚠️  SENDGRID_API_KEY not set (optional for email)")
        return False
    
    try:
        from sendgrid import SendGridAPIClient
        
        sg = SendGridAPIClient(api_key)
        # Just test connection, don't send email
        
        print(f"   ✅ SendGrid configured")
        return True
    except Exception as e:
        print(f"   ❌ SendGrid error: {e}")
        return False


async def test_database():
    """Test database connection"""
    print("\n🗄️  Testing Database...")
    
    db_url = os.getenv('DATABASE_URL', 'sqlite:///arbitrage.db')
    
    try:
        from sqlalchemy import create_engine
        
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        print(f"   ✅ Database connected successfully")
        print(f"      URL: {db_url.split('@')[0]}...")
        return True
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False


async def test_all():
    """Test all APIs"""
    
    print("=" * 60)
    print("API CONNECTION TESTER")
    print("=" * 60)
    
    results = {}
    
    # Test each API
    results['openai'] = await test_openai()
    results['database'] = await test_database()
    results['keepa'] = await test_keepa()
    results['bookscouter'] = await test_bookscouter()
    results['twilio'] = await test_twilio()
    results['sendgrid'] = await test_sendgrid()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    total = len(results)
    working = sum(1 for v in results.values() if v)
    
    print(f"\n✅ {working}/{total} services working")
    
    if working < 2:
        print("\n⚠️  WARNING: Core services not configured!")
        print("   Minimum required: OpenAI + Database")
    elif working < 4:
        print("\n⚠️  System partially configured")
        print("   Recommended: Add Keepa + BookScouter for best results")
    else:
        print("\n✅ System ready to run!")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_all())

