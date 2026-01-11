"""
Database initialization script for PostgreSQL
Creates required tables if they don't exist
"""

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS arbitrage_db;

-- Connect to database
\c arbitrage_db;

-- Create enum types
CREATE TYPE opportunity_status AS ENUM ('pending', 'approved', 'rejected', 'purchased');
CREATE TYPE product_category AS ENUM (
    'books', 'trading_cards', 'video_games', 'musical_instruments', 
    'lego', 'sporting_goods', 'baby_equipment', 'electronics', 
    'photography', 'tools', 'other'
);
CREATE TYPE decision_type AS ENUM ('PURCHASE', 'NEGOTIATE', 'SKIP', 'RESEARCH');

-- Create opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id SERIAL PRIMARY KEY,
    source_marketplace VARCHAR(100) NOT NULL,
    source_price DECIMAL(10, 2) NOT NULL,
    target_marketplace VARCHAR(100) NOT NULL,
    target_price DECIMAL(10, 2),
    product_title TEXT NOT NULL,
    product_category product_category DEFAULT 'other',
    product_condition VARCHAR(50),
    seller_info JSONB,
    estimated_profit DECIMAL(10, 2),
    profit_margin DECIMAL(5, 4),
    roi DECIMAL(5, 4),
    estimated_fees DECIMAL(10, 2),
    risk_score DECIMAL(3, 2),
    ai_decision decision_type,
    ai_confidence DECIMAL(3, 2),
    ai_reasoning TEXT,
    status opportunity_status DEFAULT 'pending',
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create purchases table
CREATE TABLE IF NOT EXISTS purchases (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id),
    purchase_price DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    transaction_id VARCHAR(200),
    seller_contact TEXT,
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expected_delivery DATE,
    tracking_number VARCHAR(200),
    status VARCHAR(50) DEFAULT 'pending',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(id),
    marketplace VARCHAR(100) NOT NULL,
    listing_id VARCHAR(200),
    sale_price DECIMAL(10, 2) NOT NULL,
    marketplace_fees DECIMAL(10, 2) DEFAULT 0,
    shipping_fees DECIMAL(10, 2) DEFAULT 0,
    total_revenue DECIMAL(10, 2),
    net_profit DECIMAL(10, 2),
    sold_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    buyer_info JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create listings table
CREATE TABLE IF NOT EXISTS listings (
    id SERIAL PRIMARY KEY,
    purchase_id INTEGER REFERENCES purchases(id),
    marketplace VARCHAR(100) NOT NULL,
    listing_id VARCHAR(200),
    title TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    condition VARCHAR(50),
    images JSONB,
    status VARCHAR(50) DEFAULT 'active',
    views INTEGER DEFAULT 0,
    favorites INTEGER DEFAULT 0,
    listed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create negotiations table
CREATE TABLE IF NOT EXISTS negotiations (
    id SERIAL PRIMARY KEY,
    opportunity_id INTEGER REFERENCES opportunities(id),
    target_price DECIMAL(10, 2) NOT NULL,
    current_offer DECIMAL(10, 2),
    attempts INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',
    messages JSONB,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_opportunities_category ON opportunities(product_category);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);
CREATE INDEX IF NOT EXISTS idx_opportunities_discovered ON opportunities(discovered_at);
CREATE INDEX IF NOT EXISTS idx_opportunities_profit ON opportunities(estimated_profit);
CREATE INDEX IF NOT EXISTS idx_purchases_status ON purchases(status);
CREATE INDEX IF NOT EXISTS idx_purchases_date ON purchases(purchased_at);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sold_at);
CREATE INDEX IF NOT EXISTS idx_listings_marketplace ON listings(marketplace);
CREATE INDEX IF NOT EXISTS idx_listings_status ON listings(status);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers
CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO arbitrage_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO arbitrage_user;

-- Insert sample data for testing (optional)
-- Uncomment if needed for development
/*
INSERT INTO opportunities (
    source_marketplace, source_price, target_marketplace, target_price,
    product_title, product_category, product_condition, estimated_profit,
    profit_margin, ai_decision, ai_confidence
) VALUES (
    'Facebook Marketplace', 25.00, 'Amazon', 45.00,
    'College Textbook - Introduction to Psychology', 'books', 'Used - Good',
    15.00, 0.35, 'PURCHASE', 0.85
);
*/

-- Success message
SELECT 'Database initialized successfully!' as status;
