"""
Demo Mode - See the system in action without API keys
Simulates the complete arbitrage workflow
"""

import asyncio
import random
from datetime import datetime
from loguru import logger
import yaml
from pathlib import Path

# Configure logger
logger.add(
    "logs/demo_{time}.log",
    rotation="1 day",
    level="INFO"
)

class DemoArbitrageSystem:
    """Demo version of the arbitrage system"""
    
    def __init__(self):
        logger.info("=" * 80)
        logger.info("🤖 AI ARBITRAGE SYSTEM - DEMO MODE")
        logger.info("=" * 80)
        logger.info("Running in DEMO mode to show capabilities")
        logger.info("Add API keys in .env to run in PRODUCTION mode")
        logger.info("=" * 80)
        
        self.stats = {
            'opportunities_found': 0,
            'negotiations_started': 0,
            'purchases_completed': 0,
            'profit_earned': 0.0
        }
    
    def generate_demo_opportunity(self, category: str) -> dict:
        """Generate realistic demo opportunity"""
        
        opportunities = {
            'books': [
                ("Calculus Early Transcendentals 10th Ed", 45.00, 89.99),
                ("Organic Chemistry 8th Edition", 38.00, 125.00),
                ("Physics for Scientists Engineers", 52.00, 98.00),
                ("Medical Terminology Systems", 28.00, 78.50),
            ],
            'video_games': [
                ("Nintendo Switch OLED - Like New", 220.00, 349.99),
                ("PS5 Games Bundle - Sealed", 85.00, 159.99),
                ("Pokemon Legends Arceus - New", 32.00, 54.99),
            ],
            'trading_cards': [
                ("Pokemon Booster Box Sealed", 125.00, 245.00),
                ("Magic The Gathering Collection", 89.00, 185.00),
                ("Pokemon Charizard PSA 9", 280.00, 520.00),
            ]
        }
        
        category_opps = opportunities.get(category, opportunities['books'])
        title, buy_price, sell_price = random.choice(category_opps)
        
        fees = sell_price * 0.15 + 3.50  # Amazon fees
        profit = sell_price - buy_price - fees
        margin = profit / sell_price
        
        return {
            'title': title,
            'buy_price': buy_price,
            'sell_price': sell_price,
            'estimated_fees': fees,
            'estimated_profit': profit,
            'profit_margin': margin,
            'category': category,
            'marketplace': random.choice(['Facebook Marketplace', 'Craigslist', 'OfferUp']),
            'seller_rating': round(random.uniform(4.0, 5.0), 1),
            'location': 'Boston, MA'
        }
    
    async def demo_workflow(self):
        """Demonstrate complete workflow"""
        
        logger.info("\n🔍 PHASE 1: MARKET SCANNING")
        logger.info("Scanning marketplaces for opportunities...")
        await asyncio.sleep(2)
        
        categories = ['books', 'video_games', 'trading_cards']
        
        for category in categories:
            logger.info(f"  📊 Scanning {category}...")
            await asyncio.sleep(1)
            
            # Generate demo opportunities
            for _ in range(random.randint(3, 7)):
                opp = self.generate_demo_opportunity(category)
                self.stats['opportunities_found'] += 1
                
                await self.demo_analyze_opportunity(opp)
        
        logger.info(f"\n✅ Scanning complete! Found {self.stats['opportunities_found']} opportunities")
        
        # Show stats
        await asyncio.sleep(2)
        self.print_stats()
    
    async def demo_analyze_opportunity(self, opp: dict):
        """Demo AI analysis"""
        
        logger.info(f"\n🤖 Analyzing: {opp['title']}")
        await asyncio.sleep(0.5)
        
        # Calculate metrics
        logger.info(f"  💰 Buy Price: ${opp['buy_price']:.2f}")
        logger.info(f"  📈 Sell Price: ${opp['sell_price']:.2f}")
        logger.info(f"  💵 Estimated Profit: ${opp['estimated_profit']:.2f}")
        logger.info(f"  📊 Profit Margin: {opp['profit_margin']*100:.1f}%")
        logger.info(f"  🏪 Source: {opp['marketplace']}")
        logger.info(f"  ⭐ Seller Rating: {opp['seller_rating']}/5.0")
        
        # AI decision logic
        if opp['profit_margin'] > 0.30 and opp['estimated_profit'] > 25:
            decision = "PURCHASE"
            confidence = 0.92
            logger.info(f"  ✅ AI Decision: {decision} (Confidence: {confidence:.0%})")
            logger.info(f"  🎯 Action: Execute purchase immediately!")
            
            await self.demo_purchase(opp)
            
        elif opp['profit_margin'] > 0.20 and opp['estimated_profit'] > 15:
            decision = "NEGOTIATE"
            confidence = 0.85
            target_price = opp['buy_price'] * 0.85
            
            logger.info(f"  💬 AI Decision: {decision} (Confidence: {confidence:.0%})")
            logger.info(f"  📝 AI Message: 'Hi! Interested in your {opp['title'][:30]}...")
            logger.info(f"             Would you take ${target_price:.2f}? I can pick up today!'")
            
            self.stats['negotiations_started'] += 1
            
            # Simulate negotiation
            if random.random() > 0.4:  # 60% success rate
                logger.info(f"  ✅ Seller accepted ${target_price:.2f}!")
                opp['buy_price'] = target_price
                opp['estimated_profit'] = opp['sell_price'] - target_price - opp['estimated_fees']
                await self.demo_purchase(opp)
            else:
                logger.info(f"  ❌ Seller declined - moving to next opportunity")
        else:
            logger.info(f"  ⏭️  AI Decision: SKIP (Margin {opp['profit_margin']*100:.1f}% below threshold)")
    
    async def demo_purchase(self, opp: dict):
        """Demo purchase execution"""
        
        logger.info(f"  💳 Processing purchase...")
        await asyncio.sleep(1)
        logger.info(f"  ✅ Purchase completed: ${opp['buy_price']:.2f}")
        
        self.stats['purchases_completed'] += 1
        self.stats['profit_earned'] += opp['estimated_profit']
        
        # Demo listing
        await asyncio.sleep(0.5)
        logger.info(f"  📝 Creating Amazon listing...")
        await asyncio.sleep(1)
        logger.info(f"  ✅ Listed on Amazon FBA: ${opp['sell_price']:.2f}")
        logger.info(f"  🎯 Expected profit when sold: ${opp['estimated_profit']:.2f}")
    
    def print_stats(self):
        """Print session statistics"""
        
        logger.info("\n" + "=" * 80)
        logger.info("📊 DEMO SESSION STATISTICS")
        logger.info("=" * 80)
        logger.info(f"🔍 Opportunities Found:     {self.stats['opportunities_found']}")
        logger.info(f"💬 Negotiations Started:    {self.stats['negotiations_started']}")
        logger.info(f"✅ Purchases Completed:     {self.stats['purchases_completed']}")
        logger.info(f"💰 Total Profit Expected:   ${self.stats['profit_earned']:.2f}")
        
        if self.stats['purchases_completed'] > 0:
            avg_profit = self.stats['profit_earned'] / self.stats['purchases_completed']
            logger.info(f"📈 Average Profit/Item:     ${avg_profit:.2f}")
        
        logger.info("=" * 80)
        logger.info("\n✨ This is a DEMO showing system capabilities")
        logger.info("To run in PRODUCTION mode:")
        logger.info("  1. Add your API keys to .env file")
        logger.info("  2. Run: python main.py")
        logger.info("\nTo see the dashboard:")
        logger.info("  docker-compose up -d")
        logger.info("  Open: http://localhost:3000")
        logger.info("=" * 80)

async def main():
    """Run demo"""
    
    try:
        system = DemoArbitrageSystem()
        await system.demo_workflow()
        
    except KeyboardInterrupt:
        logger.info("\n\nDemo stopped by user")
    except Exception as e:
        logger.exception(f"Demo error: {e}")

if __name__ == "__main__":
    # Create logs directory
    Path("logs").mkdir(exist_ok=True)
    
    asyncio.run(main())

