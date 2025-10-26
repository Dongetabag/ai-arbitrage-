#!/bin/bash

# Startup script for AI Arbitrage System

echo "=================================="
echo " AI ARBITRAGE SYSTEM - STARTUP"
echo "=================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/bin/pip" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found!"
    echo "Run the setup wizard first:"
    echo "  python scripts/quick_start.py"
    echo ""
    exit 1
fi

# Check if database exists
if [ ! -f "arbitrage.db" ]; then
    echo "Initializing database..."
    python scripts/init_db.py
fi

# Test API connections
echo ""
echo "Testing API connections..."
python scripts/test_apis.py

echo ""
read -p "Start the arbitrage system? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting AI Arbitrage System..."
    echo "Press Ctrl+C to stop"
    echo ""
    
    python main.py
else
    echo "Startup cancelled"
fi

