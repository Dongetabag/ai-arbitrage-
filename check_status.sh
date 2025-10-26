#!/bin/bash

# Status Checker for AI Arbitrage System

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║  📊 AI ARBITRAGE SYSTEM - STATUS CHECK                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

echo "🔍 Checking Docker services..."
echo ""

# Check if docker-compose is running
if docker-compose ps 2>/dev/null | grep -q "Up"; then
    echo "✅ SYSTEM IS RUNNING!"
    echo ""
    docker-compose ps
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  🌐 ACCESS YOUR DASHBOARD                                ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "  📊 Dashboard:    http://localhost:3000"
    echo "  🐍 Python API:   http://localhost:8000"
    echo "  📘 NestJS API:   http://localhost:3001"
    echo "  📚 API Docs:     http://localhost:8000/docs"
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║  💡 QUICK COMMANDS                                       ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo "  View logs:       docker-compose logs -f"
    echo "  Stop system:     docker-compose down"
    echo "  Restart:         docker-compose restart"
    echo ""
else
    echo "⏳ System is starting or not running yet..."
    echo ""
    echo "If you just ran 'docker-compose up -d':"
    echo "  • First-time image download takes 2-3 minutes"
    echo "  • Services need 30-60 seconds to start"
    echo "  • Run this script again in 1 minute"
    echo ""
    echo "To start the system:"
    echo "  docker-compose up -d"
    echo ""
    echo "To check detailed status:"
    echo "  docker-compose ps"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════"
echo ""

