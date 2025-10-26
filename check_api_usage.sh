#!/bin/bash
# Check if system is using the correct API (Gemini vs OpenAI)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 CHECKING AI API CONFIGURATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check .env file
if [ -f .env ]; then
    echo "📄 .env file configuration:"
    echo ""
    grep "AI_PROVIDER" .env || echo "  ⚠️  AI_PROVIDER not set"
    grep "AI_MODEL" .env || echo "  ⚠️  AI_MODEL not set"
    echo ""
    
    if grep -q "AI_PROVIDER=google" .env; then
        echo "✅ CORRECT: Using Google Gemini (FREE)"
    elif grep -q "AI_PROVIDER=openai" .env; then
        echo "❌ WARNING: Using OpenAI (EXPENSIVE)"
        echo "   Change AI_PROVIDER to 'google' to use FREE Gemini"
    fi
    echo ""
    
    if grep -q "GOOGLE_API_KEY=your-google-api-key-here" .env; then
        echo "⚠️  Google API key not configured yet"
        echo "   Get one at: https://makersuite.google.com/app/apikey"
    elif grep -q "GOOGLE_API_KEY=AIza" .env; then
        echo "✅ Google API key configured"
    fi
    echo ""
    
    if grep -q "^OPENAI_API_KEY=sk-" .env; then
        echo "⚠️  OpenAI API key is set (will incur charges if used)"
        echo "   Consider commenting it out with # to prevent accidental use"
    fi
else
    echo "❌ .env file not found"
    echo "   Run the setup script to create it"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 CHECKING RUNNING PROCESSES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

PROCESSES=$(ps aux | grep -i "python.*main.py\|python.*arbitrage" | grep -v grep)

if [ -z "$PROCESSES" ]; then
    echo "✅ No arbitrage processes running"
    echo "   (No API charges being incurred)"
else
    echo "⚠️  Arbitrage process is running:"
    echo "$PROCESSES"
    echo ""
    echo "   To stop it: pkill -f 'python.*main.py'"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 CHECK YOUR API USAGE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "OpenAI Usage:  https://platform.openai.com/account/usage"
echo "Google Gemini: https://makersuite.google.com/app/apikey"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

