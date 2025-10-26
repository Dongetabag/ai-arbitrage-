"""
Database Models
SQLAlchemy models for all system entities
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, 
    ForeignKey, Text, JSON, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class OpportunityStatus(enum.Enum):
    DISCOVERED = "discovered"
    ANALYZING = "analyzing"
    NEGOTIATING = "negotiating"
    PURCHASING = "purchasing"
    PURCHASED = "purchased"
    LISTING = "listing"
    LISTED = "listed"
    SOLD = "sold"
    SKIPPED = "skipped"
    FAILED = "failed"


class ProductCategory(enum.Enum):
    BOOKS = "books"
    TRADING_CARDS = "trading_cards"
    VIDEO_GAMES = "video_games"
    MUSICAL_INSTRUMENTS = "musical_instruments"
    LEGO = "lego"
    SPORTING_GOODS = "sporting_goods"
    BABY_EQUIPMENT = "baby_equipment"
    ELECTRONICS = "electronics"
    PHOTOGRAPHY = "photography"
    TOOLS = "tools"


class Opportunity(Base):
    """Arbitrage opportunities discovered by the system"""
    __tablename__ = 'opportunities'
    
    id = Column(Integer, primary_key=True)
    external_id = Column(String(255), unique=True, index=True)
    
    # Product details
    product_title = Column(String(500), nullable=False)
    product_description = Column(Text)
    product_category = Column(SQLEnum(ProductCategory), nullable=False, index=True)
    product_condition = Column(String(50))
    product_images = Column(JSON)  # List of image URLs
    product_metadata = Column(JSON)  # Additional product data
    
    # Source marketplace
    source_marketplace = Column(String(100), nullable=False, index=True)
    source_url = Column(Text)
    source_price = Column(Float, nullable=False)
    source_listing_date = Column(DateTime)
    
    # Seller information
    seller_name = Column(String(255))
    seller_rating = Column(Float)
    seller_review_count = Column(Integer)
    seller_response_rate = Column(Float)
    seller_location = Column(String(255))
    seller_contact = Column(String(500))
    seller_metadata = Column(JSON)
    
    # Target marketplace
    target_marketplace = Column(String(100), nullable=False)
    target_price = Column(Float, nullable=False)
    target_price_source = Column(String(100))  # Keepa, CamelCamelCamel, etc.
    
    # Financial calculations
    estimated_fees = Column(Float, default=0.0)
    estimated_shipping = Column(Float, default=0.0)
    estimated_profit = Column(Float)
    profit_margin = Column(Float)
    roi = Column(Float)
    
    # Risk assessment
    risk_score = Column(Float, default=0.0)
    requires_authentication = Column(Boolean, default=False)
    
    # AI analysis
    ai_decision = Column(String(50))
    ai_confidence = Column(Float)
    ai_reasoning = Column(Text)
    
    # Status tracking
    status = Column(SQLEnum(OpportunityStatus), default=OpportunityStatus.DISCOVERED, index=True)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    analyzed_at = Column(DateTime)
    purchased_at = Column(DateTime)
    listed_at = Column(DateTime)
    sold_at = Column(DateTime)
    
    # Relationships
    negotiations = relationship("Negotiation", back_populates="opportunity")
    purchase = relationship("Purchase", back_populates="opportunity", uselist=False)
    listing = relationship("Listing", back_populates="opportunity", uselist=False)
    
    def __repr__(self):
        return f"<Opportunity {self.id}: {self.product_title[:50]} - ${self.estimated_profit:.2f}>"


class Negotiation(Base):
    """Negotiation attempts with sellers"""
    __tablename__ = 'negotiations'
    
    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'), nullable=False)
    
    # Negotiation details
    offer_amount = Column(Float, nullable=False)
    message_sent = Column(Text)
    response_received = Column(Text)
    
    # Status
    status = Column(String(50))  # sent, accepted, countered, rejected
    sent_at = Column(DateTime, default=datetime.utcnow)
    responded_at = Column(DateTime)
    
    # AI generated content
    generated_by_ai = Column(Boolean, default=True)
    ai_strategy = Column(Text)
    
    opportunity = relationship("Opportunity", back_populates="negotiations")


class Purchase(Base):
    """Completed purchases"""
    __tablename__ = 'purchases'
    
    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'), nullable=False)
    
    # Purchase details
    final_price = Column(Float, nullable=False)
    payment_method = Column(String(50))
    transaction_id = Column(String(255))
    
    # Receipt/confirmation
    confirmation_number = Column(String(255))
    receipt_url = Column(Text)
    receipt_data = Column(JSON)
    
    # Fulfillment
    pickup_location = Column(String(500))
    pickup_scheduled_at = Column(DateTime)
    received_at = Column(DateTime)
    
    # Status
    status = Column(String(50))  # pending, confirmed, received, cancelled
    purchased_at = Column(DateTime, default=datetime.utcnow)
    
    opportunity = relationship("Opportunity", back_populates="purchase")


class Listing(Base):
    """Products listed for sale"""
    __tablename__ = 'listings'
    
    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'), nullable=False)
    
    # Listing details
    marketplace = Column(String(100), nullable=False)
    listing_id = Column(String(255))
    listing_url = Column(Text)
    
    # Pricing
    list_price = Column(Float, nullable=False)
    sale_price = Column(Float)
    
    # Content
    title = Column(String(500))
    description = Column(Text)
    bullet_points = Column(JSON)
    images = Column(JSON)
    
    # Performance
    views_count = Column(Integer, default=0)
    watchers_count = Column(Integer, default=0)
    questions_count = Column(Integer, default=0)
    
    # Status
    status = Column(String(50))  # active, sold, cancelled, suspended
    listed_at = Column(DateTime, default=datetime.utcnow)
    sold_at = Column(DateTime)
    
    opportunity = relationship("Opportunity", back_populates="listing")
    sales = relationship("Sale", back_populates="listing")


class Sale(Base):
    """Completed sales"""
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    
    # Sale details
    sale_price = Column(Float, nullable=False)
    buyer_username = Column(String(255))
    buyer_email = Column(String(255))
    
    # Fees and costs
    marketplace_fees = Column(Float, default=0.0)
    payment_processing_fees = Column(Float, default=0.0)
    shipping_cost = Column(Float, default=0.0)
    
    # Profit calculation
    total_revenue = Column(Float)
    total_costs = Column(Float)
    net_profit = Column(Float)
    actual_margin = Column(Float)
    actual_roi = Column(Float)
    
    # Fulfillment
    tracking_number = Column(String(255))
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    
    # Status
    status = Column(String(50))  # pending, shipped, delivered, refunded
    sold_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    listing = relationship("Listing", back_populates="sales")
    support_tickets = relationship("SupportTicket", back_populates="sale")


class SupportTicket(Base):
    """Customer support interactions"""
    __tablename__ = 'support_tickets'
    
    id = Column(Integer, primary_key=True)
    sale_id = Column(Integer, ForeignKey('sales.id'))
    
    # Ticket details
    customer_name = Column(String(255))
    customer_email = Column(String(255))
    customer_phone = Column(String(50))
    
    subject = Column(String(500))
    category = Column(String(100))  # shipping, returns, product_question, etc.
    priority = Column(String(50), default='normal')
    
    # Status
    status = Column(String(50), default='open')  # open, in_progress, resolved, closed
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime)
    
    # Relationships
    sale = relationship("Sale", back_populates="support_tickets")
    messages = relationship("SupportMessage", back_populates="ticket")


class SupportMessage(Base):
    """Individual messages in support tickets"""
    __tablename__ = 'support_messages'
    
    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('support_tickets.id'), nullable=False)
    
    # Message details
    sender = Column(String(50))  # customer, agent, ai
    message = Column(Text, nullable=False)
    
    # AI metadata
    generated_by_ai = Column(Boolean, default=False)
    ai_confidence = Column(Float)
    
    sent_at = Column(DateTime, default=datetime.utcnow)
    
    ticket = relationship("SupportTicket", back_populates="messages")


class PriceHistory(Base):
    """Historical pricing data for products"""
    __tablename__ = 'price_history'
    
    id = Column(Integer, primary_key=True)
    
    # Product identification
    product_identifier = Column(String(255), index=True)  # ASIN, UPC, SKU, etc.
    identifier_type = Column(String(50))
    marketplace = Column(String(100), index=True)
    
    # Price data
    price = Column(Float, nullable=False)
    sales_rank = Column(Integer)
    in_stock = Column(Boolean)
    
    # Source
    data_source = Column(String(100))  # Keepa, CamelCamelCamel, manual
    
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)


class SystemMetrics(Base):
    """System performance metrics"""
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    
    # Performance
    opportunities_scanned = Column(Integer, default=0)
    opportunities_analyzed = Column(Integer, default=0)
    purchases_attempted = Column(Integer, default=0)
    purchases_completed = Column(Integer, default=0)
    listings_created = Column(Integer, default=0)
    sales_completed = Column(Integer, default=0)
    
    # Financial
    total_spent = Column(Float, default=0.0)
    total_revenue = Column(Float, default=0.0)
    total_profit = Column(Float, default=0.0)
    
    # Time period
    date = Column(DateTime, default=datetime.utcnow, index=True)
    period = Column(String(50))  # hourly, daily, weekly, monthly


class APIUsage(Base):
    """Track API usage and costs"""
    __tablename__ = 'api_usage'
    
    id = Column(Integer, primary_key=True)
    
    api_name = Column(String(100), nullable=False, index=True)
    endpoint = Column(String(255))
    
    # Usage
    request_count = Column(Integer, default=1)
    success = Column(Boolean, default=True)
    response_time_ms = Column(Integer)
    
    # Costs
    estimated_cost = Column(Float, default=0.0)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class Blacklist(Base):
    """Blacklisted sellers, products, or keywords"""
    __tablename__ = 'blacklist'
    
    id = Column(Integer, primary_key=True)
    
    type = Column(String(50), nullable=False)  # seller, product, keyword
    value = Column(String(500), nullable=False, index=True)
    reason = Column(Text)
    
    added_at = Column(DateTime, default=datetime.utcnow)
    added_by = Column(String(100))  # user, system, ai
    
    active = Column(Boolean, default=True)

