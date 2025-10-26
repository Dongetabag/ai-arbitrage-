# Complete Marketplace Integration List

## Primary Buying Sources (Currently Implemented)

### Local Marketplaces
1. **Facebook Marketplace** ✅
   - URL: https://www.facebook.com/marketplace
   - Scan Interval: Every 10 minutes
   - Best For: Local deals, furniture, electronics
   - Integration: Selenium scraping

2. **Craigslist** ✅
   - URL: https://craigslist.org
   - Locations: Boston, Worcester, Springfield
   - Scan Interval: Every 10 minutes
   - Best For: All categories, especially bulk
   - Integration: HTTP scraping

3. **OfferUp** ✅
   - URL: https://offerup.com
   - Scan Interval: Every 15 minutes
   - Best For: Electronics, sporting goods
   - Integration: Web scraping

4. **Letgo** (Merged with OfferUp)
   - Now part of OfferUp platform

5. **VarageSale**
   - URL: https://www.varagesale.com
   - Best For: Local community sales
   - Integration: Requires account

6. **Mercari** ✅
   - URL: https://www.mercari.com
   - Scan Interval: Every 15 minutes
   - Best For: Fashion, collectibles, electronics
   - Integration: API + scraping

7. **Nextdoor**
   - URL: https://nextdoor.com
   - Best For: Hyper-local deals
   - Integration: Requires neighborhood verification

8. **5miles**
   - URL: https://www.5miles.com
   - Best For: Local marketplace
   - Integration: Mobile app primarily

## National Marketplaces

9. **eBay** ✅
   - URL: https://www.ebay.com
   - Best For: All categories
   - Integration: eBay Finding API

10. **Amazon Warehouse Deals**
    - URL: https://www.amazon.com/Warehouse-Deals
    - Best For: Open box, damaged packaging
    - Integration: Amazon PA-API

## Specialty Book Sources

11. **ThriftBooks**
    - URL: https://www.thriftbooks.com
    - Best For: Bulk used books

12. **AbeBooks**
    - URL: https://www.abebooks.com
    - Best For: Rare/collectible books

13. **Half Price Books**
    - URL: https://www.hpb.com
    - Best For: Local book stores

14. **Local College Bookstores** (100+ in Boston area)
    - MIT Coop
    - Harvard Coop
    - BU Bookstore
    - Northeastern Bookstore
    - And 95+ more

## Retail Clearance Sites

15. **Target Clearance**
    - Check: RedCard exclusive deals
    - Best Time: End of season

16. **Walmart Rollbacks**
    - Check: Clearance sections
    - Best Time: Weekly

17. **Best Buy Open Box**
    - URL: https://www.bestbuy.com/site/open-box
    - Check: Open box and clearance

18. **Home Depot Special Buys**
    - Check: Daily special buy section

19. **Lowe's Clearance**
    - Check: End caps and clearance

20. **Dick's Sporting Goods**
    - Check: Seasonal clearance

21. **REI Garage Sale**
    - URL: https://www.rei.com/used
    - Best For: Returned outdoor gear

22. **TJ Maxx/Marshall's**
    - In-store only, compare prices

## Liquidation/Wholesale

23. **B-Stock Solutions**
    - URL: https://www.bstocksupply.com
    - Best For: Amazon returns, overstock

24. **Bulq.com**
    - URL: https://bulq.com
    - Best For: Bulk lots

25. **Direct Liquidation**
    - URL: https://www.directliquidation.com
    - Best For: Pallets and lots

26. **Liquidation.com**
    - URL: https://www.liquidation.com
    - Best For: Large liquidation pallets

## Auction Sites

27. **GovDeals**
    - URL: https://www.govdeals.com
    - Best For: Government surplus

28. **PropertyRoom**
    - URL: https://www.propertyroom.com
    - Best For: Police auctions

29. **AuctionZip**
    - URL: https://www.auctionzip.com
    - Best For: Estate sales

## Specialty Sites by Category

### Trading Cards
30. **TCGPlayer**
    - URL: https://www.tcgplayer.com
    - Integration: TCGPlayer API

31. **Card Kingdom**
    - URL: https://www.cardkingdom.com

32. **eBay Trading Cards**
    - Filter for ending auctions

### Video Games
33. **GameStop Used**
    - URL: https://www.gamestop.com/trades
    - Check: Pre-owned section

34. **DKOldies**
    - URL: https://www.dkoldies.com
    - Best For: Retro games

### Musical Instruments
35. **Reverb.com** ✅
    - URL: https://reverb.com
    - Integration: Reverb API

36. **Guitar Center Used**
    - URL: https://www.guitarcenter.com/Used

37. **Sweetwater Used**
    - URL: https://www.sweetwater.com/used

### Photography
38. **KEH Camera**
    - URL: https://www.keh.com
    - Best For: Used camera equipment

39. **MPB.com**
    - URL: https://www.mpb.com
    - Best For: Camera gear

40. **B&H Used**
    - URL: https://www.bhphotovideo.com/c/buy/Used

### Sporting Goods
41. **Play It Again Sports**
    - URL: https://www.playitagainsports.com
    - Best For: Used sports equipment

42. **SidelineSwap**
    - URL: https://www.sidelineswap.com
    - Best For: Team sports gear

43. **Golf Avenue**
    - URL: https://www.golfavenue.com
    - Best For: Golf equipment

### Baby Equipment
44. **Once Upon a Child**
    - URL: https://www.onceuponachild.com
    - Best For: Used baby gear

45. **Kid to Kid**
    - URL: https://www.kidtokid.com

46. **Kidizen**
    - URL: https://www.kidizen.com

## Selling Platforms (Where You List)

### Primary
1. **Amazon FBA** ✅ (Primary)
   - Highest volume
   - Best for: All categories
   - Fees: 15% + FBA fees

2. **eBay** ✅ (Secondary)
   - Good for collectibles
   - Fees: 12.9% + PayPal

### Secondary
3. **Facebook Marketplace**
   - Local sales
   - No fees

4. **Mercari**
   - Good for fashion/collectibles
   - 10% fee

## Integration Status

### ✅ Fully Integrated
- Facebook Marketplace (scraping)
- Craigslist (scraping)
- OfferUp (scraping)
- eBay (API + scraping)
- Mercari (scraping)
- Amazon FBA (SP-API for listing)
- Keepa (pricing)
- BookScouter (book pricing)

### 🔨 Partially Integrated
- TCGPlayer (API wrapper ready)
- PriceCharting (API wrapper ready)
- Reverb (API wrapper ready)
- BrickLink (API wrapper ready)
- BuyBotPro (API wrapper ready)

### ⏳ Planned
- Nextdoor
- Liquidation sites
- Additional retail clearance monitoring
- Authentication services (Entrupy, LegitCheck)

## Adding New Marketplaces

To add a new marketplace:

1. Create scanner class in `monitoring/market_scanner.py`:
```python
class NewMarketplaceScanner(MarketplaceScanner):
    async def scan(self, category: str, keywords: List[str]) -> List[Dict]:
        # Implementation
        pass
```

2. Register in `settings.yaml`:
```yaml
marketplaces:
  new_marketplace:
    enabled: true
    scan_interval: 15
```

3. Add to scanner initialization in `MarketScanner.__init__`

## Best Practices

### For Buying
- **Facebook/Craigslist**: Best for local pickup, cash deals
- **eBay**: Good for auction sniping, Buy It Now deals
- **Liquidation Sites**: Bulk purchasing, higher risk

### For Selling
- **Amazon FBA**: Best for high-volume, hands-off
- **eBay**: Good for unique/collectible items
- **Local**: Best for large/heavy items (avoid shipping)

### Timing
- **Morning** (6-9am): Check overnight listings
- **Lunch** (12-2pm): People list during break
- **Evening** (5-8pm): High listing activity
- **Late Night** (10pm-1am): Desperate sellers, best deals

### Location Strategy
- Set location to college towns for textbooks
- Beach towns for sporting goods (off-season)
- Affluent suburbs for electronics/luxury goods
- Military bases (via GovDeals) for tools/equipment

