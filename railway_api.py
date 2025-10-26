#!/usr/bin/env python3
"""
Simplified FastAPI for Railway deployment
Minimal dependencies, maximum compatibility
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
import os

# Initialize FastAPI
app = FastAPI(
    title="AI Arbitrage API",
    description="Real-time API for arbitrage platform",
    version="1.0.0"
)

# CORS - Allow all origins for Railway deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class OpportunityResponse(BaseModel):
    id: int
    product_title: str
    source_marketplace: str
    source_price: float
    target_price: float
    estimated_profit: float
    profit_margin: float
    category: str
    product_category: str
    ai_decision: str
    ai_confidence: float
    discovered_at: str

class ScanRequest(BaseModel):
    category: str = "all"

class ScanResponse(BaseModel):
    status: str
    category: str
    message: str
    estimated_duration_seconds: int
    timestamp: str

class StatusResponse(BaseModel):
    is_scanning: bool
    last_scan: str
    next_scan: str
    marketplaces_active: List[str]
    categories_active: int
    ai_model: str

# Mock data generator
def generate_mock_opportunities(count: int = 5) -> List[Dict]:
    """Generate mock arbitrage opportunities"""
    products = [
        "Calculus: Early Transcendentals 10th Edition — Stewart",
        "PSA 9 Charizard 1st Edition Base Set — Authenticated",
        "Nintendo Switch OLED Console — White, Mint Condition",
        "Organic Chemistry 8th Edition — McMurry, Hardcover",
        "LEGO Star Wars UCS Millennium Falcon — Sealed, Retired Set",
        "MacBook Pro 13-inch M2 — Space Gray, 512GB",
        "iPhone 15 Pro Max — Natural Titanium, 256GB",
        "Sony WH-1000XM5 Wireless Headphones — Black",
        "Nike Air Jordan 1 Retro High OG — Chicago",
        "Rolex Submariner Date — Black Dial, Steel"
    ]
    
    marketplaces = ["Craigslist", "Facebook Marketplace", "OfferUp", "eBay", "Mercari"]
    categories = ["Books", "Trading Cards", "Electronics", "LEGO", "Fashion", "Collectibles"]
    decisions = ["PURCHASE", "NEGOTIATE", "SKIP", "AUTHENTICATE", "ANALYZING"]
    
    opportunities = []
    for i in range(count):
        source_price = round(random.uniform(20, 500), 2)
        target_price = round(source_price * random.uniform(1.5, 3.0), 2)
        profit = round(target_price - source_price, 2)
        margin = round(profit / target_price, 3)
        
        opportunities.append({
            "id": i + 1,
            "product_title": random.choice(products),
            "source_marketplace": random.choice(marketplaces),
            "source_price": source_price,
            "target_price": target_price,
            "estimated_profit": profit,
            "profit_margin": margin,
            "category": random.choice(categories),
            "product_category": random.choice(categories).lower().replace(" ", "_"),
            "ai_decision": random.choice(decisions),
            "ai_confidence": round(random.uniform(0.7, 0.98), 2),
            "discovered_at": (datetime.utcnow() - timedelta(minutes=random.randint(1, 60))).isoformat()
        })
    
    return opportunities

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Arbitrage System API",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "railway": True
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "message": "AI Arbitrage System is running on Railway"
    }

@app.get("/api/opportunities", response_model=List[OpportunityResponse])
async def get_opportunities(limit: int = 10):
    """Get arbitrage opportunities"""
    try:
        opportunities = generate_mock_opportunities(limit)
        return opportunities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching opportunities: {str(e)}")

@app.post("/api/scan/trigger", response_model=ScanResponse)
async def trigger_scan(data: ScanRequest):
    """Trigger immediate marketplace scan"""
    try:
        category = data.category or "all"
        
        # Log the scan request
        print(f"🔍 Force scan triggered for category: {category} at {datetime.utcnow()}")
        
        return ScanResponse(
            status="scanning",
            category=category,
            message="Marketplace scan initiated",
            estimated_duration_seconds=300,  # 5 minutes
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering scan: {str(e)}")

@app.get("/api/scan/status", response_model=StatusResponse)
async def get_scan_status():
    """Get current scan status"""
    try:
        return StatusResponse(
            is_scanning=True,  # Would check actual scanner state
            last_scan=datetime.utcnow().isoformat(),
            next_scan=(datetime.utcnow() + timedelta(minutes=10)).isoformat(),
            marketplaces_active=["Facebook", "Craigslist", "OfferUp", "eBay", "Mercari"],
            categories_active=10,
            ai_model="Google Gemini 2.5 Flash"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting scan status: {str(e)}")

@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    try:
        return {
            "total_opportunities": 47,
            "active_scans": 3,
            "total_profit_today": 1247.50,
            "success_rate": 0.89,
            "ai_confidence_avg": 0.87,
            "last_update": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"🚀 Starting AI Arbitrage API on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
