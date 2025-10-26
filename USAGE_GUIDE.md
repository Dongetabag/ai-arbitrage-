# Usage Guide - AI Arbitrage System

## Getting Started

### Initial Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your .env file
cp .env.example .env
# Edit .env with your API keys

# 3. Test API connections
python scripts/test_apis.py

# 4. Initialize database
python scripts/init_db.py

# 5. Start the system
python main.py
```

## How the System Works

### 1. Market Monitoring Phase
The system continuously scans these marketplaces every 10-60 minutes:

- **Facebook Marketplace** (every 10 min)
- **Craigslist** (every 10 min)
- **OfferUp** (every 15 min)
- **eBay** (every 15 min)
- **Mercari** (every 15 min)

**What it looks for:**
- Items in your enabled categories
- Prices below market value
- Good seller ratings
- Local availability

### 2. AI Analysis Phase
For each found item, the AI:

1. **Identifies the product** - Extracts ISBN, UPC, model number
2. **Checks current market price** - Using Keepa, BookScouter, etc.
3. **Calculates profit** - Subtracts all fees and shipping
4. **Assesses risk** - Seller rating, item condition, fraud potential
5. **Makes decision:**
   - ✅ **PURCHASE** - Meets all criteria, profitable
   - 💬 **NEGOTIATE** - Profitable if price reduced
   - ❌ **SKIP** - Not profitable or too risky
   - 🔍 **AUTHENTICATE** - Needs verification first

### 3. Negotiation Phase (if applicable)
The AI automatically:

1. Generates personalized negotiation message
2. Contacts seller (SMS, email, or marketplace message)
3. Makes initial offer (typically 15-20% below asking)
4. Handles counter-offers (up to 3 rounds)
5. Accepts deal if profitable margin achieved

**Example negotiation:**
```
Seller asks: $80
AI offers: $65 (19% discount)
Seller counters: $72
AI accepts if margin still >20%
```

### 4. Purchase Phase
When deal is agreed:

**Automated platforms (eBay):**
- Places order automatically
- Processes payment
- Confirms purchase

**Manual platforms (Craigslist, Facebook):**
- Sends you notification
- Provides pickup details
- Waits for manual confirmation

**Safety check:** Auto-purchase disabled by default for items over $100

### 5. Listing Phase
After successful purchase:

1. **AI generates optimized listing:**
   - SEO-friendly title
   - Compelling description
   - Bullet points highlighting value

2. **Lists on target marketplace:**
   - Amazon FBA (primary)
   - eBay (secondary)
   - Facebook Marketplace (manual)

3. **Sets competitive price:**
   - Ensures minimum margin
   - Prices just below competition
   - Uses psychological pricing (.99)

### 6. Customer Support Phase
When buyer asks questions or has issues:

1. **AI analyzes inquiry** - Categorizes as shipping, return, question, etc.
2. **Generates response** - Professional, empathetic, helpful
3. **Auto-responds** (if confidence >80%) OR flags for review
4. **Escalates** if keywords detected: refund, lawyer, scam, etc.

**Response time:** < 30 seconds for simple inquiries

## Daily Workflow

### Morning Routine
```bash
# Check overnight opportunities
python scripts/daily_report.py

# Review pending purchases (if auto_purchase=false)
python scripts/review_purchases.py

# Approve or skip each one
```

### Throughout the Day
The system runs autonomously:
- Scans marketplaces continuously
- Negotiates with sellers
- Creates listings
- Handles customer support

### Evening Review
```bash
# View daily stats
python scripts/daily_stats.py

# Shows:
# - Opportunities found
# - Negotiations started
# - Purchases made
# - Listings created
# - Sales completed
# - Profit earned
```

## Configuration Options

### Conservative Mode (Recommended for start)
```yaml
# config/settings.yaml
automation:
  auto_purchase: false    # Review all purchases manually
  auto_list: true         # Auto-create listings
  auto_negotiate: true    # Let AI negotiate
  auto_respond_support: false  # Review support responses

risk_management:
  max_purchase_per_item: 100    # Low limit
  max_daily_spend: 500          # Conservative
  min_profit_margin: 0.25       # High margin requirement
```

### Aggressive Mode (After validation)
```yaml
automation:
  auto_purchase: true     # Fully autonomous
  auto_list: true
  auto_negotiate: true
  auto_respond_support: true

risk_management:
  max_purchase_per_item: 500
  max_daily_spend: 2000
  min_profit_margin: 0.20
```

## Maximizing Profits

### 1. Focus on High-Margin Categories
Start with:
1. **Books/Textbooks** (47.3% margin) - Easiest, lowest risk
2. **Trading Cards** (36.8% margin) - Higher value, needs authentication
3. **Video Games** (34.2% margin) - Good volume

### 2. Timing Matters
- **Textbooks:** Scan heavily in August (fall semester) and January (spring)
- **Toys/LEGO:** Peak in October-December
- **Sporting Goods:** End of season clearance

### 3. Location Optimization
Set your location to college towns for textbooks:
- Boston, MA (100+ colleges)
- Austin, TX
- Ann Arbor, MI
- Berkeley, CA

### 4. Rapid Response
- First to contact seller = 80% success rate
- Respond within 1 hour of listing

## Monitoring Performance

### Key Metrics
```python
# View in database or logs
- Conversion rate: Opportunities → Purchases
- Negotiation success rate
- Average profit per item
- ROI by category
- Inventory turnover time
```

### Alerts
You'll receive notifications for:
- High-profit opportunities (>$100 profit)
- Successful purchases
- Sales completed
- Customer support escalations
- Daily spending limit reached

## Troubleshooting

**Not finding opportunities?**
- Check if categories are enabled in config
- Verify API keys are working
- Expand search radius
- Add more keywords

**Low profit margins?**
- Increase min_margin in config
- Focus on top 3 categories
- Enable more pricing APIs for accuracy

**Negotiations failing?**
- AI might be too aggressive
- Try increasing initial offer amount
- Some sellers don't negotiate

**Slow sales?**
- Check listing prices vs competition
- Improve listing photos
- Enhance descriptions
- Verify items are in-stock on Amazon

## Advanced Usage

### Custom Categories
Add your own profitable categories:

```yaml
categories:
  custom_category:
    enabled: true
    avg_margin: 0.30
    min_margin: 0.20
    max_purchase_price: 300
    scan_interval_minutes: 30
```

### Blacklisting
Block problematic sellers or products:

```python
# Add to database
from database.models import Blacklist

blacklist = Blacklist(
    type='seller',
    value='scammy_seller_123',
    reason='Multiple bad transactions'
)
```

### Price Tracking
Monitor specific products over time:

```python
# The system automatically tracks prices
# Query price_history table for trends
```

## Expected Performance

**Conservative estimates (first month):**
- 50-100 opportunities found per day
- 10-20 negotiations started
- 5-10 purchases completed
- $20-50 profit per item
- **$500-1,500 monthly profit**

**After optimization (month 3+):**
- 200-300 opportunities found per day
- 40-60 purchases per week
- $2,000-5,000 monthly profit
- 15-25% average margin
- ROI: 30-50%

## Support & Help

Check logs for detailed information:
```bash
tail -f logs/arbitrage_*.log
```

For questions or issues, review:
- README.md - System overview
- API_SETUP_GUIDE.md - API configuration
- Database models in database/models.py
- Config options in config/settings.yaml

