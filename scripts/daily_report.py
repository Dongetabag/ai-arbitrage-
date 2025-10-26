"""
Daily Report Generator
Shows opportunities, purchases, and profit for the day
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy import func

sys.path.insert(0, str(Path(__file__).parent.parent))

from database.db_manager import DatabaseManager
from database.models import Opportunity, Purchase, Sale, OpportunityStatus
import yaml


def load_config():
    """Load configuration"""
    with open('config/settings.yaml', 'r') as f:
        return yaml.safe_load(f)


def generate_daily_report():
    """Generate and print daily report"""
    
    config = load_config()
    db = DatabaseManager(config)
    session = db.get_session()
    
    # Get today's date range
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    
    print("\n" + "=" * 80)
    print(f"DAILY REPORT - {today.strftime('%A, %B %d, %Y')}")
    print("=" * 80)
    
    # Opportunities discovered
    opportunities = session.query(Opportunity).filter(
        Opportunity.discovered_at >= today,
        Opportunity.discovered_at < tomorrow
    ).all()
    
    print(f"\n📊 OPPORTUNITIES DISCOVERED: {len(opportunities)}")
    
    if opportunities:
        # Group by status
        by_status = {}
        for opp in opportunities:
            status = opp.status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        for status, count in sorted(by_status.items()):
            print(f"   {status:20s}: {count:3d}")
        
        # Top opportunities
        top_opps = sorted(opportunities, key=lambda x: x.estimated_profit or 0, reverse=True)[:5]
        
        print(f"\n💰 TOP 5 OPPORTUNITIES:")
        for i, opp in enumerate(top_opps, 1):
            profit = opp.estimated_profit or 0
            margin = (opp.profit_margin or 0) * 100
            print(f"   {i}. {opp.product_title[:50]:50s} - ${profit:6.2f} ({margin:.0f}%)")
    
    # Purchases
    purchases = session.query(Purchase).filter(
        Purchase.purchased_at >= today,
        Purchase.purchased_at < tomorrow
    ).all()
    
    print(f"\n🛒 PURCHASES COMPLETED: {len(purchases)}")
    
    if purchases:
        total_spent = sum(p.final_price for p in purchases)
        print(f"   Total Spent: ${total_spent:,.2f}")
        
        for i, purchase in enumerate(purchases, 1):
            opp = purchase.opportunity
            print(f"   {i}. {opp.product_title[:50]:50s} - ${purchase.final_price:.2f}")
    
    # Sales
    sales = session.query(Sale).filter(
        Sale.sold_at >= today,
        Sale.sold_at < tomorrow
    ).all()
    
    print(f"\n💵 SALES COMPLETED: {len(sales)}")
    
    if sales:
        total_revenue = sum(s.total_revenue or 0 for s in sales)
        total_profit = sum(s.net_profit or 0 for s in sales)
        
        print(f"   Total Revenue: ${total_revenue:,.2f}")
        print(f"   Total Profit:  ${total_profit:,.2f}")
        
        if total_revenue > 0:
            avg_margin = (total_profit / total_revenue) * 100
            print(f"   Avg Margin:    {avg_margin:.1f}%")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    opportunities_analyzed = len(opportunities)
    purchase_rate = (len(purchases) / opportunities_analyzed * 100) if opportunities_analyzed > 0 else 0
    
    total_spent = sum(p.final_price for p in purchases)
    total_revenue = sum(s.total_revenue or 0 for s in sales)
    total_profit = sum(s.net_profit or 0 for s in sales)
    
    print(f"\nOpportunities → Purchases: {purchase_rate:.1f}%")
    print(f"Money In Circulation: ${total_spent:,.2f}")
    print(f"Money Returned: ${total_revenue:,.2f}")
    print(f"Net Profit Today: ${total_profit:,.2f}")
    
    print("\n" + "=" * 80)
    
    session.close()


if __name__ == "__main__":
    try:
        generate_daily_report()
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)

