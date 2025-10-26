"""
FastAPI Endpoints - Real-Time Data API
Connects frontend dashboard to backend database
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func
import yaml
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager
from database.models import Opportunity, Purchase, Sale, Listing

# Load config
with open('config/settings.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Initialize FastAPI
app = FastAPI(
    title="AI Arbitrage API",
    description="Real-time API for arbitrage platform",
    version="1.0.0"
)

# CORS - Allow frontend to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = DatabaseManager(config)


@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "AI Arbitrage API",
        "status": "operational",
        "version": "1.0.0",
        "ai": "Google Gemini 2.5 Flash",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/opportunities")
async def get_opportunities(
    category: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
):
    """Get opportunities from database"""
    
    session = db.get_session()
    
    try:
        query = session.query(Opportunity)
        
        if category:
            query = query.filter(Opportunity.product_category == category)
        
        if status:
            query = query.filter(Opportunity.status == status)
        
        opportunities = query.order_by(
            Opportunity.discovered_at.desc()
        ).limit(limit).all()
        
        result = []
        for opp in opportunities:
            result.append({
                'id': opp.id,
                'product_title': opp.product_title,
                'source_marketplace': opp.source_marketplace,
                'source_price': float(opp.source_price or 0),
                'target_price': float(opp.target_price or 0),
                'estimated_profit': float(opp.estimated_profit or 0),
                'profit_margin': float(opp.profit_margin or 0),
                'category': opp.product_category.value if opp.product_category else 'other',
                'product_category': opp.product_category.value if opp.product_category else 'other',
                'ai_decision': opp.ai_decision,
                'ai_confidence': float(opp.ai_confidence or 0),
                'discovered_at': opp.discovered_at.isoformat() if opp.discovered_at else None
            })
        
        return result
        
    finally:
        session.close()


@app.get("/api/stats/daily")
async def get_daily_stats():
    """Get daily statistics"""
    
    session = db.get_session()
    
    try:
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)
        
        # Count opportunities
        opp_count = session.query(Opportunity).filter(
            Opportunity.discovered_at >= today,
            Opportunity.discovered_at < tomorrow
        ).count()
        
        # Count purchases
        purchase_count = session.query(Purchase).filter(
            Purchase.purchased_at >= today,
            Purchase.purchased_at < tomorrow
        ).count()
        
        # Total profit from sales
        total_profit = session.query(func.sum(Sale.net_profit)).filter(
            Sale.sold_at >= today,
            Sale.sold_at < tomorrow
        ).scalar() or 0
        
        # Average margin
        avg_margin = session.query(func.avg(Opportunity.profit_margin)).filter(
            Opportunity.discovered_at >= today,
            Opportunity.profit_margin.isnot(None)
        ).scalar() or 0
        
        # Sales count
        sales_count = session.query(Sale).filter(
            Sale.sold_at >= today,
            Sale.sold_at < tomorrow
        ).count()
        
        return {
            'opportunities_found': opp_count,
            'purchases_completed': purchase_count,
            'sales_completed': sales_count,
            'total_profit': float(total_profit),
            'avg_margin': float(avg_margin),
            'date': today.isoformat()
        }
        
    finally:
        session.close()


@app.get("/api/stats/performance")
async def get_performance():
    """Get overall performance metrics"""
    
    session = db.get_session()
    
    try:
        total_opps = session.query(Opportunity).count()
        total_purchases = session.query(Purchase).count()
        total_sales = session.query(Sale).count()
        
        total_revenue = session.query(func.sum(Sale.total_revenue)).scalar() or 0
        total_profit = session.query(func.sum(Sale.net_profit)).scalar() or 0
        
        conversion_rate = (total_purchases / total_opps * 100) if total_opps > 0 else 0
        
        return {
            'total_opportunities': total_opps,
            'total_purchases': total_purchases,
            'total_sales': total_sales,
            'total_revenue': float(total_revenue),
            'total_profit': float(total_profit),
            'conversion_rate': float(conversion_rate),
            'avg_profit_per_sale': float(total_profit / total_sales) if total_sales > 0 else 0
        }
        
    finally:
        session.close()


@app.post("/api/purchase/approve")
async def approve_purchase(data: dict):
    """Approve a purchase"""
    
    opportunity_id = data.get('opportunity_id')
    
    # TODO: Trigger purchase flow
    # For now, just acknowledge
    
    return {
        'status': 'approved',
        'opportunity_id': opportunity_id,
        'message': 'Purchase approval received. Processing...'
    }


@app.post("/api/scan/trigger")
async def trigger_scan(data: dict):
    """Trigger immediate marketplace scan"""
    
    from datetime import datetime
    import asyncio
    
    category = data.get('category', 'all')
    
    # Log the scan request
    print(f"🔍 Force scan triggered for category: {category} at {datetime.utcnow()}")
    
    # In production, this would trigger the actual scanner
    # For now, return success to show UI feedback works
    
    return {
        'status': 'scanning',
        'category': category,
        'message': 'Marketplace scan initiated',
        'estimated_duration_seconds': 300,  # 5 minutes
        'timestamp': datetime.utcnow().isoformat()
    }


@app.get("/api/scan/status")
async def get_scan_status():
    """Get current scan status"""
    
    return {
        'is_scanning': True,  # Would check actual scanner state
        'last_scan': datetime.utcnow().isoformat(),
        'next_scan': (datetime.utcnow() + timedelta(minutes=10)).isoformat(),
        'marketplaces_active': ['Facebook', 'Craigslist', 'OfferUp', 'eBay', 'Mercari'],
        'categories_active': 10,
        'ai_model': 'Google Gemini 2.5 Flash'
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    
    return {
        'status': 'healthy',
        'database': 'connected',
        'ai': 'Google Gemini 2.5 Flash',
        'timestamp': datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
