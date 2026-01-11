"""
FastAPI Endpoints - Real-Time Data API
Connects frontend dashboard to backend database
"""

import os
import sys
import yaml
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from sqlalchemy import func, text

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager
from database.models import Opportunity, Purchase, Sale, Listing

# Initialize FastAPI
app = FastAPI(
    title="AI Arbitrage API",
    description="Real-time API for arbitrage platform with AI-powered decision making",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None,
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

# Error Handler Middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    """Global error handling"""
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Internal server error",
                "message": str(e) if os.getenv("ENVIRONMENT") == "development" else "An error occurred",
                "timestamp": datetime.utcnow().isoformat()
            }
        )

# CORS Configuration
cors_origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else [
    "http://localhost:3000",
    "http://localhost:3001",
]

# Add Vercel URL if exists
if vercel_url := os.getenv("VERCEL_URL"):
    cors_origins.append(f"https://{vercel_url}")

# Add specific frontend URL if provided
if frontend_url := os.getenv("FRONTEND_URL"):
    cors_origins.append(frontend_url)

logger.info(f"CORS origins configured: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize database with proper error handling
db = None
try:
    config_path = Path('config/settings.yaml')
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logger.info("Configuration loaded from settings.yaml")
    else:
        # Use environment variables for Railway/production
        config = {
            'database': {
                'url': os.getenv('DATABASE_URL', 'sqlite:///arbitrage.db')
            }
        }
        logger.info("Using environment-based configuration")
    
    db = DatabaseManager(config)
    logger.info("Database manager initialized successfully")
except Exception as e:
    logger.warning(f"Database initialization failed: {e}. Running in limited mode.")
    db = None



@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "AI Arbitrage API",
        "status": "operational",
        "version": "1.0.0",
        "ai": "Google Gemini 2.5 Flash",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway and production monitoring"""
    health_status = {
        "status": "healthy",
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development"),
        "service": "ai-arbitrage-api",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "ai_model": "Google Gemini 2.5 Flash"
    }
    
    # Check database connectivity
    if db:
        try:
            session = db.get_session()
            session.execute(text("SELECT 1"))
            session.close()
            health_status["database"] = "connected"
        except Exception as e:
            health_status["status"] = "degraded"
            health_status["database"] = f"error: {str(e)[:50]}"
            logger.error(f"Database health check failed: {e}")
    else:
        health_status["database"] = "not configured"
    
    return health_status

# Add OPTIONS handler for preflight CORS requests
@app.options("/{path:path}")
async def options_handler(path: str):
    return {"status": "ok"}


@app.get("/api/opportunities")
async def get_opportunities(
    category: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50
):
    """Get opportunities from database"""
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )
    
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
    except Exception as e:
        logger.error(f"Error fetching opportunities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving opportunities"
        )
    finally:
        session.close()


@app.get("/api/stats/daily")
async def get_daily_stats():
    """Get daily statistics"""
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
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
    except Exception as e:
        logger.error(f"Error fetching daily stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving daily statistics"
        )
    finally:
        session.close()


@app.get("/api/stats/performance")
async def get_performance():
    """Get overall performance metrics"""
    
    if not db:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available"
        )
    
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
    except Exception as e:
        logger.error(f"Error fetching performance stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving performance statistics"
        )
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


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"🚀 Starting AI Arbitrage API on {host}:{port}")
    uvicorn.run(app, host=host, port=port, workers=2)
