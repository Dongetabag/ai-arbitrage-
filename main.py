"""
Main Application Entry Point
Orchestrates the entire AI arbitrage system
"""

import asyncio
import yaml
from pathlib import Path
from loguru import logger
from datetime import datetime
import sys
from typing import Dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.ai_engine import AIReasoningEngine, ArbitrageOpportunity
from monitoring.market_scanner import MarketScanner, PriceValidator
from communication.seller_communicator import SellerCommunicator, NegotiationManager
from purchasing.purchase_engine import PurchaseEngine
from selling.listing_manager import ListingManager
from support.customer_support import CustomerSupportAI
from integrations.api_integrations import APIManager
from database.db_manager import DatabaseManager


class ArbitrageSystem:
    """
    Main orchestrator for the AI arbitrage system
    """
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        """Initialize the system"""
        
        logger.info("=" * 80)
        logger.info("AI ARBITRAGE SYSTEM - GOLD MINE")
        logger.info("=" * 80)
        
        # Load configuration
        self.config = self._load_config(config_path)
        logger.info(f"Configuration loaded from {config_path}")
        
        # Initialize database
        self.db = DatabaseManager(self.config)
        logger.info("Database initialized")
        
        # Initialize core components
        self.ai_engine = AIReasoningEngine(self.config)
        self.market_scanner = MarketScanner(self.config)
        self.price_validator = PriceValidator(self.config)
        self.communicator = SellerCommunicator(self.config)
        self.negotiation_manager = NegotiationManager(self.ai_engine, self.communicator, self.config)
        self.purchase_engine = PurchaseEngine(self.config)
        self.listing_manager = ListingManager(self.ai_engine, self.config)
        self.customer_support = CustomerSupportAI(self.ai_engine, self.config)
        self.api_manager = APIManager()
        
        logger.info("All modules initialized successfully")
        
        # System state
        self.running = False
        self.stats = {
            'opportunities_found': 0,
            'negotiations_started': 0,
            'purchases_completed': 0,
            'listings_created': 0,
            'sales_completed': 0,
            'total_profit': 0.0
        }
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        
        config_file = Path(config_path)
        
        if not config_file.exists():
            logger.error(f"Configuration file not found: {config_path}")
            raise FileNotFoundError(f"Config file missing: {config_path}")
        
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    async def start(self):
        """Start the arbitrage system"""
        
        logger.info("Starting AI Arbitrage System...")
        self.running = True
        
        # Start main loops
        tasks = [
            self.market_monitoring_loop(),
            self.negotiation_monitoring_loop(),
            self.listing_monitoring_loop(),
            self.support_monitoring_loop()
        ]
        
        await asyncio.gather(*tasks)
    
    async def market_monitoring_loop(self):
        """Main loop for monitoring marketplaces"""
        
        logger.info("Market monitoring loop started")
        
        while self.running:
            try:
                # Scan all categories
                opportunities = await self.market_scanner.scan_all_categories()
                
                self.stats['opportunities_found'] += len(opportunities)
                
                logger.info(f"Found {len(opportunities)} potential opportunities")
                
                # Process each opportunity
                for opp_data in opportunities:
                    await self.process_opportunity(opp_data)
                
                # Wait before next scan
                await asyncio.sleep(600)  # 10 minutes
                
            except Exception as e:
                logger.error(f"Market monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def process_opportunity(self, opp_data: Dict):
        """Process a discovered opportunity"""
        
        try:
            category = opp_data.get('category', '')
            
            # Validate pricing
            validation = await self.price_validator.validate_opportunity(opp_data, category)
            
            if not validation or not validation.get('viable'):
                logger.debug(f"Opportunity not viable: {opp_data['title'][:50]}")
                return
            
            # Create opportunity object
            opportunity = ArbitrageOpportunity(
                source_marketplace=opp_data['marketplace'],
                source_price=opp_data['price'],
                target_marketplace='amazon',  # Default
                target_price=validation['target_price'],
                product_title=opp_data['title'],
                product_category=category,
                product_condition=opp_data.get('condition', 'Used'),
                seller_info={
                    'location': opp_data.get('location', ''),
                    'contact': opp_data.get('seller_contact', '')
                },
                profit_margin=validation['profit_margin'],
                roi=validation['roi'],
                estimated_fees=validation['estimated_fees'],
                risk_score=0.0,
                metadata=opp_data
            )
            
            # Assess risk
            opportunity.risk_score = self.ai_engine.assess_risk(opportunity)
            
            # Get AI decision
            decision = self.ai_engine.analyze_opportunity(opportunity)
            
            # Save to database
            opp_id = await self.db.save_opportunity(opportunity, decision)
            
            # Act on decision
            if decision.decision.value == 'PURCHASE':
                if self.ai_engine.should_purchase(opportunity):
                    logger.info(f"✓ PURCHASING: {opportunity.product_title[:50]}")
                    await self.execute_purchase(opportunity)
                    
            elif decision.decision.value == 'NEGOTIATE':
                logger.info(f"↔ NEGOTIATING: {opportunity.product_title[:50]}")
                target_price = decision.action_params.get('target_price', opportunity.source_price * 0.85)
                await self.negotiation_manager.initiate_negotiation(
                    opportunity=opportunity.__dict__,
                    target_price=target_price
                )
                self.stats['negotiations_started'] += 1
            
            else:
                logger.debug(f"✗ SKIPPING: {opportunity.product_title[:50]} - {decision.reasoning[:100]}")
            
        except Exception as e:
            logger.error(f"Error processing opportunity: {e}")
    
    async def execute_purchase(self, opportunity: ArbitrageOpportunity):
        """Execute a purchase"""
        
        try:
            result = await self.purchase_engine.execute_purchase(
                opportunity=opportunity.__dict__,
                final_price=opportunity.source_price,
                payment_method='auto'
            )
            
            if result['success']:
                self.stats['purchases_completed'] += 1
                logger.success(f"Purchase completed: {opportunity.product_title[:50]}")
                
                # Immediately create listing
                await self.create_listing_for_purchase(opportunity, result)
            else:
                logger.error(f"Purchase failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"Purchase execution error: {e}")
    
    async def create_listing_for_purchase(self, opportunity: ArbitrageOpportunity, purchase_result: Dict):
        """Create listing after successful purchase"""
        
        try:
            # Calculate optimal listing price
            cost_basis = opportunity.source_price + opportunity.estimated_fees
            target_margin = 0.25  # 25% margin
            list_price = cost_basis / (1 - target_margin)
            
            # Round to psychological price point
            list_price = round(list_price - 0.01, 2)  # e.g., $19.99
            
            product_data = {
                'title': opportunity.product_title,
                'category': opportunity.product_category,
                'condition': opportunity.product_condition,
                'features': opportunity.metadata.get('features', []),
                'brand': opportunity.metadata.get('brand', ''),
                'images': opportunity.metadata.get('images', [])
            }
            
            result = await self.listing_manager.create_listing(
                product=product_data,
                target_marketplace=opportunity.target_marketplace,
                price=list_price
            )
            
            if result['success']:
                self.stats['listings_created'] += 1
                logger.success(f"Listing created: {result.get('listing_url', 'N/A')}")
            else:
                logger.error(f"Listing failed: {result.get('error')}")
                
        except Exception as e:
            logger.error(f"Listing creation error: {e}")
    
    async def negotiation_monitoring_loop(self):
        """Monitor ongoing negotiations"""
        
        logger.info("Negotiation monitoring loop started")
        
        while self.running:
            try:
                # Check for seller responses
                # Update negotiation status
                # Handle counter offers
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Negotiation monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def listing_monitoring_loop(self):
        """Monitor active listings"""
        
        logger.info("Listing monitoring loop started")
        
        while self.running:
            try:
                # Check for sales
                # Update prices based on competition
                # Handle customer questions
                
                await asyncio.sleep(300)  # Check every 5 minutes
                
            except Exception as e:
                logger.error(f"Listing monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def support_monitoring_loop(self):
        """Monitor customer support tickets"""
        
        logger.info("Support monitoring loop started")
        
        while self.running:
            try:
                # Check for new support tickets
                # Generate AI responses
                # Send responses if auto-respond enabled
                
                await asyncio.sleep(180)  # Check every 3 minutes
                
            except Exception as e:
                logger.error(f"Support monitoring error: {e}")
                await asyncio.sleep(60)
    
    def stop(self):
        """Stop the system"""
        logger.info("Stopping AI Arbitrage System...")
        self.running = False
    
    def print_stats(self):
        """Print current statistics"""
        logger.info("=" * 80)
        logger.info("SYSTEM STATISTICS")
        logger.info("=" * 80)
        logger.info(f"Opportunities Found: {self.stats['opportunities_found']}")
        logger.info(f"Negotiations Started: {self.stats['negotiations_started']}")
        logger.info(f"Purchases Completed: {self.stats['purchases_completed']}")
        logger.info(f"Listings Created: {self.stats['listings_created']}")
        logger.info(f"Sales Completed: {self.stats['sales_completed']}")
        logger.info(f"Total Profit: ${self.stats['total_profit']:.2f}")
        logger.info("=" * 80)


async def main():
    """Main entry point"""
    
    # Configure logging
    logger.add(
        "logs/arbitrage_{time}.log",
        rotation="1 day",
        retention="30 days",
        level="INFO"
    )
    
    try:
        # Initialize system
        system = ArbitrageSystem()
        
        # Start the system
        await system.start()
        
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
        system.stop()
        system.print_stats()
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

