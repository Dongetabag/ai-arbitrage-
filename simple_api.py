#!/usr/bin/env python3
"""
Ultra-simple FastAPI for Railway deployment
No external dependencies, guaranteed to work
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

# Initialize FastAPI
app = FastAPI(title="AI Arbitrage API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI Arbitrage System API",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "railway": True
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/opportunities")
async def opportunities():
    return [
        {
            "id": 1,
            "product_title": "Test Product",
            "source_marketplace": "Test Marketplace",
            "source_price": 100.0,
            "target_price": 150.0,
            "estimated_profit": 50.0,
            "profit_margin": 0.33,
            "category": "Test",
            "ai_decision": "PURCHASE",
            "ai_confidence": 0.95
        }
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"🚀 Starting simple API on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
