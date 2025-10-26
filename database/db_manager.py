"""
Database Manager
Handles all database operations
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger

from database.models import (
    Base, Opportunity, Negotiation, Purchase, Listing, Sale,
    SupportTicket, SupportMessage, PriceHistory, SystemMetrics,
    APIUsage, Blacklist, OpportunityStatus, ProductCategory
)


class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.engine = self._create_engine()
        self.SessionLocal = sessionmaker(bind=self.engine)
        
        # Create tables
        self._create_tables()
    
    def _create_engine(self):
        """Create database engine"""
        
        db_url = os.getenv('DATABASE_URL', 'sqlite:///arbitrage.db')
        
        engine = create_engine(
            db_url,
            echo=False,
            pool_pre_ping=True
        )
        
        logger.info(f"Database engine created: {db_url.split('@')[0]}...")
        return engine
    
    def _create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)
        logger.info("Database tables created/verified")
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    async def save_opportunity(self, opportunity, decision) -> int:
        """Save discovered opportunity to database"""
        
        session = self.get_session()
        
        try:
            opp = Opportunity(
                product_title=opportunity.product_title,
                product_category=ProductCategory[opportunity.product_category.upper()],
                product_condition=opportunity.product_condition,
                source_marketplace=opportunity.source_marketplace,
                source_price=opportunity.source_price,
                target_marketplace=opportunity.target_marketplace,
                target_price=opportunity.target_price,
                estimated_fees=opportunity.estimated_fees,
                estimated_profit=decision.estimated_profit,
                profit_margin=opportunity.profit_margin,
                roi=opportunity.roi,
                risk_score=opportunity.risk_score,
                ai_decision=decision.decision.value,
                ai_confidence=decision.confidence,
                ai_reasoning=decision.reasoning,
                status=OpportunityStatus.DISCOVERED
            )
            
            session.add(opp)
            session.commit()
            session.refresh(opp)
            
            logger.debug(f"Opportunity saved: ID {opp.id}")
            
            return opp.id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save opportunity: {e}")
            return -1
        finally:
            session.close()
    
    async def save_negotiation(self, negotiation_data: Dict) -> int:
        """Save negotiation attempt"""
        
        session = self.get_session()
        
        try:
            neg = Negotiation(
                opportunity_id=negotiation_data.get('opportunity_id'),
                offer_amount=negotiation_data.get('offer_amount'),
                message_sent=negotiation_data.get('message_sent'),
                status=negotiation_data.get('status'),
                generated_by_ai=True
            )
            
            session.add(neg)
            session.commit()
            session.refresh(neg)
            
            return neg.id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save negotiation: {e}")
            return -1
        finally:
            session.close()
    
    async def save_purchase(self, purchase_data: Dict) -> int:
        """Save completed purchase"""
        
        session = self.get_session()
        
        try:
            purchase = Purchase(
                opportunity_id=purchase_data.get('opportunity_id'),
                final_price=purchase_data.get('final_price'),
                payment_method=purchase_data.get('payment_method'),
                transaction_id=purchase_data.get('transaction_id'),
                status=purchase_data.get('status', 'completed')
            )
            
            session.add(purchase)
            session.commit()
            session.refresh(purchase)
            
            logger.info(f"Purchase saved: ID {purchase.id}")
            
            return purchase.id
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to save purchase: {e}")
            return -1
        finally:
            session.close()
    
    async def get_daily_spend(self) -> float:
        """Get total spending for today"""
        
        session = self.get_session()
        
        try:
            today = datetime.utcnow().date()
            
            total = session.query(Purchase).filter(
                Purchase.purchased_at >= today
            ).with_entities(
                func.sum(Purchase.final_price)
            ).scalar()
            
            return float(total or 0.0)
            
        finally:
            session.close()
    
    async def get_active_negotiations(self) -> List[Negotiation]:
        """Get all active negotiations"""
        
        session = self.get_session()
        
        try:
            negotiations = session.query(Negotiation).filter(
                Negotiation.status == 'sent'
            ).all()
            
            return negotiations
            
        finally:
            session.close()
    
    async def update_metrics(self, metrics: Dict):
        """Update system metrics"""
        
        session = self.get_session()
        
        try:
            metric = SystemMetrics(
                opportunities_scanned=metrics.get('opportunities_scanned', 0),
                opportunities_analyzed=metrics.get('opportunities_analyzed', 0),
                purchases_completed=metrics.get('purchases_completed', 0),
                listings_created=metrics.get('listings_created', 0),
                sales_completed=metrics.get('sales_completed', 0),
                total_spent=metrics.get('total_spent', 0.0),
                total_revenue=metrics.get('total_revenue', 0.0),
                total_profit=metrics.get('total_profit', 0.0),
                period='hourly'
            )
            
            session.add(metric)
            session.commit()
            
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update metrics: {e}")
        finally:
            session.close()

