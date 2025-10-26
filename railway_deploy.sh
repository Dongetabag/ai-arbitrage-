#!/bin/bash

echo "🚀 Deploying AI Arbitrage Backend to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

echo "🔐 Logging into Railway..."
railway login

echo "📦 Initializing Railway project..."
railway init

echo "🔧 Setting environment variables..."
railway variables set GOOGLE_API_KEY=AIzaSyBOXCq6SjXVOJg7ulD4CT8FoMEvf-wq2ng
railway variables set AI_PROVIDER=google
railway variables set AI_MODEL=gemini-2.5-flash
railway variables set DATABASE_URL=sqlite:///arbitrage.db
railway variables set PORT=8000
railway variables set HOST=0.0.0.0

echo "🚀 Deploying to Railway..."
railway up

echo "🌐 Getting deployment URL..."
BACKEND_URL=$(railway domain)
echo "✅ Backend deployed to: $BACKEND_URL"

echo "🎊 DEPLOYMENT COMPLETE!"
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: http://localhost:3001"
echo "Full Stack: ✅ LIVE"
