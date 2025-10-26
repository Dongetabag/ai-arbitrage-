"""
Market Scanner
Monitors marketplaces for arbitrage opportunities
"""

import os
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
import httpx
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MarketplaceScanner(ABC):
    """Base class for marketplace scanners"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.name = self.__class__.__name__
        
    @abstractmethod
    async def scan(self, category: str, keywords: List[str]) -> List[Dict]:
        """Scan marketplace for opportunities"""
        pass
    
    def filter_results(self, results: List[Dict], max_price: float) -> List[Dict]:
        """Filter results based on criteria"""
        filtered = []
        for item in results:
            if item.get('price', float('inf')) <= max_price:
                filtered.append(item)
        return filtered


class FacebookMarketplaceScanner(MarketplaceScanner):
    """Scanner for Facebook Marketplace"""
    
    async def scan(self, category: str, keywords: List[str]) -> List[Dict]:
        """Scan Facebook Marketplace"""
        logger.info(f"Scanning Facebook Marketplace for {category}")
        
        results = []
        
        # Note: Facebook requires authentication and has anti-scraping measures
        # This is a simplified implementation
        
        for keyword in keywords:
            try:
                # Use selenium for dynamic content
                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                driver = webdriver.Chrome(options=options)
                
                # Construct search URL
                base_url = "https://www.facebook.com/marketplace"
                location = self.config.get('location', {}).get('zipcode', '02101')
                search_url = f"{base_url}/category/search/?query={keyword}&exact=false"
                
                driver.get(search_url)
                await asyncio.sleep(3)  # Wait for dynamic content
                
                # Parse listings
                # Note: Facebook's structure changes frequently
                listings = driver.find_elements(By.CSS_SELECTOR, "[data-testid='marketplace-product-card']")
                
                for listing in listings[:20]:  # Limit to first 20
                    try:
                        title_elem = listing.find_element(By.CSS_SELECTOR, "span")
                        price_elem = listing.find_element(By.CSS_SELECTOR, "[class*='price']")
                        
                        title = title_elem.text
                        price_text = price_elem.text.replace('$', '').replace(',', '')
                        price = float(price_text) if price_text else 0
                        
                        results.append({
                            'marketplace': 'facebook_marketplace',
                            'title': title,
                            'price': price,
                            'url': listing.get_attribute('href'),
                            'category': category,
                            'discovered_at': datetime.utcnow().isoformat()
                        })
                        
                    except Exception as e:
                        logger.debug(f"Error parsing listing: {e}")
                        continue
                
                driver.quit()
                
            except Exception as e:
                logger.error(f"Facebook scan error for '{keyword}': {e}")
                
        logger.info(f"Found {len(results)} items on Facebook Marketplace")
        return results


class CraigslistScanner(MarketplaceScanner):
    """Scanner for Craigslist"""
    
    async def scan(self, category: str, keywords: List[str]) -> List[Dict]:
        """Scan Craigslist"""
        logger.info(f"Scanning Craigslist for {category}")
        
        results = []
        locations = self.config.get('craigslist_locations', ['boston', 'worcester'])
        
        async with httpx.AsyncClient() as client:
            for location in locations:
                for keyword in keywords:
                    try:
                        # Construct search URL
                        url = f"https://{location}.craigslist.org/search/sss"
                        params = {
                            'query': keyword,
                            'sort': 'date',
                            'hasPic': 1
                        }
                        
                        response = await client.get(url, params=params, timeout=30)
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Parse results
                        listings = soup.select('.result-row')
                        
                        for listing in listings[:30]:
                            try:
                                title_elem = listing.select_one('.result-title')
                                price_elem = listing.select_one('.result-price')
                                
                                if not title_elem or not price_elem:
                                    continue
                                
                                title = title_elem.text.strip()
                                price_text = price_elem.text.replace('$', '').replace(',', '')
                                price = float(price_text)
                                url = title_elem.get('href', '')
                                
                                # Get posting details
                                location_elem = listing.select_one('.result-hood')
                                location_text = location_elem.text.strip() if location_elem else ''
                                
                                results.append({
                                    'marketplace': 'craigslist',
                                    'title': title,
                                    'price': price,
                                    'url': url,
                                    'location': f"{location} {location_text}",
                                    'category': category,
                                    'discovered_at': datetime.utcnow().isoformat()
                                })
                                
                            except Exception as e:
                                logger.debug(f"Error parsing Craigslist listing: {e}")
                                continue
                                
                    except Exception as e:
                        logger.error(f"Craigslist scan error for '{keyword}' in {location}: {e}")
                    
                    await asyncio.sleep(2)  # Rate limiting
        
        logger.info(f"Found {len(results)} items on Craigslist")
        return results


class OfferUpScanner(MarketplaceScanner):
    """Scanner for OfferUp"""
    
    async def scan(self, category: str, keywords: List[str]) -> List[Dict]:
        """Scan OfferUp"""
        logger.info(f"Scanning OfferUp for {category}")
        
        results = []
        
        # OfferUp requires mobile app API or web scraping with authentication
        # This is a placeholder implementation
        
        async with httpx.AsyncClient() as client:
            for keyword in keywords:
                try:
                    url = "https://offerup.com/search/"
                    params = {
                        'q': keyword,
                        'radius': 50
                    }
                    
                    response = await client.get(url, params=params, timeout=30)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Parse results (structure varies)
                    # This is a simplified version
                    
                    logger.debug(f"OfferUp scan for '{keyword}' completed")
                    
                except Exception as e:
                    logger.error(f"OfferUp scan error: {e}")
                    
                await asyncio.sleep(2)
        
        logger.info(f"Found {len(results)} items on OfferUp")
        return results


class EbayScanner(MarketplaceScanner):
    """Scanner for eBay (for sourcing deals)"""
    
    async def scan(self, category: str, keywords: List[str]) -> List[Dict]:
        """Scan eBay for deals"""
        logger.info(f"Scanning eBay for {category}")
        
        results = []
        
        # Use eBay Finding API for better results
        # This requires eBay API credentials
        
        try:
            from ebaysdk.finding import Connection as Finding
            
            api = Finding(
                appid=os.getenv('EBAY_APP_ID'),
                config_file=None
            )
            
            for keyword in keywords:
                try:
                    response = api.execute('findItemsAdvanced', {
                        'keywords': keyword,
                        'sortOrder': 'EndTimeSoonest',
                        'itemFilter': [
                            {'name': 'ListingType', 'value': 'FixedPrice'},
                            {'name': 'Condition', 'value': 'Used'}
                        ]
                    })
                    
                    items = response.dict().get('searchResult', {}).get('item', [])
                    
                    for item in items[:20]:
                        price_data = item.get('sellingStatus', {}).get('currentPrice', {})
                        price = float(price_data.get('value', 0))
                        
                        results.append({
                            'marketplace': 'ebay',
                            'title': item.get('title', ''),
                            'price': price,
                            'url': item.get('viewItemURL', ''),
                            'item_id': item.get('itemId', ''),
                            'condition': item.get('condition', {}).get('conditionDisplayName', 'Used'),
                            'category': category,
                            'discovered_at': datetime.utcnow().isoformat()
                        })
                        
                except Exception as e:
                    logger.error(f"eBay API error for '{keyword}': {e}")
                    
                await asyncio.sleep(1)
                
        except ImportError:
            logger.warning("eBay SDK not configured, skipping eBay scan")
        except Exception as e:
            logger.error(f"eBay scanner error: {e}")
        
        logger.info(f"Found {len(results)} items on eBay")
        return results


class MercariScanner(MarketplaceScanner):
    """Scanner for Mercari"""
    
    async def scan(self, category: str, keywords: List[str]) -> List[Dict]:
        """Scan Mercari"""
        logger.info(f"Scanning Mercari for {category}")
        
        results = []
        
        async with httpx.AsyncClient() as client:
            for keyword in keywords:
                try:
                    url = "https://www.mercari.com/search/"
                    params = {
                        'keyword': keyword,
                        'status': 'on_sale'
                    }
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    }
                    
                    response = await client.get(url, params=params, headers=headers, timeout=30)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Mercari uses React, may need API endpoint or Selenium
                    # This is a placeholder
                    
                    logger.debug(f"Mercari scan for '{keyword}' completed")
                    
                except Exception as e:
                    logger.error(f"Mercari scan error: {e}")
                    
                await asyncio.sleep(2)
        
        logger.info(f"Found {len(results)} items on Mercari")
        return results


class MarketScanner:
    """
    Orchestrates scanning across all marketplaces
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.scanners = self._initialize_scanners()
        
    def _initialize_scanners(self) -> Dict[str, MarketplaceScanner]:
        """Initialize all enabled scanners"""
        scanners = {}
        
        marketplace_config = self.config.get('marketplaces', {})
        
        if marketplace_config.get('facebook_marketplace', {}).get('enabled'):
            scanners['facebook'] = FacebookMarketplaceScanner(self.config)
            
        if marketplace_config.get('craigslist', {}).get('enabled'):
            scanners['craigslist'] = CraigslistScanner(self.config)
            
        if marketplace_config.get('offerup', {}).get('enabled'):
            scanners['offerup'] = OfferUpScanner(self.config)
            
        if marketplace_config.get('ebay', {}).get('enabled'):
            scanners['ebay'] = EbayScanner(self.config)
            
        if marketplace_config.get('mercari', {}).get('enabled'):
            scanners['mercari'] = MercariScanner(self.config)
        
        logger.info(f"Initialized {len(scanners)} marketplace scanners")
        return scanners
    
    async def scan_all_categories(self) -> List[Dict]:
        """Scan all enabled categories across all marketplaces"""
        all_results = []
        
        categories = self.config.get('categories', {})
        
        for category_name, category_config in categories.items():
            if not category_config.get('enabled', False):
                continue
                
            keywords = self._get_category_keywords(category_name)
            max_price = category_config.get('max_purchase_price', 500)
            
            logger.info(f"Scanning category: {category_name}")
            
            # Scan each marketplace
            tasks = []
            for scanner_name, scanner in self.scanners.items():
                task = scanner.scan(category_name, keywords)
                tasks.append(task)
            
            # Run scans concurrently
            results_per_marketplace = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Combine results
            for results in results_per_marketplace:
                if isinstance(results, Exception):
                    logger.error(f"Scanner failed: {results}")
                    continue
                    
                # Filter by price
                filtered = scanner.filter_results(results, max_price)
                all_results.extend(filtered)
        
        logger.info(f"Total opportunities found: {len(all_results)}")
        return all_results
    
    def _get_category_keywords(self, category: str) -> List[str]:
        """Get search keywords for a category"""
        
        keyword_map = {
            'books': [
                'textbook', 'college textbook', 'used textbook',
                'hardcover book', 'first edition', 'rare book'
            ],
            'trading_cards': [
                'pokemon cards', 'magic the gathering', 'yugioh cards',
                'sports cards', 'baseball cards', 'sealed booster'
            ],
            'video_games': [
                'nintendo switch games', 'ps5 games', 'xbox games',
                'retro games', 'gameboy', 'sealed video game'
            ],
            'musical_instruments': [
                'guitar', 'keyboard', 'drum set', 'amplifier',
                'midi controller', 'audio interface', 'synthesizer'
            ],
            'lego': [
                'lego set', 'lego star wars', 'lego technic',
                'lego sealed', 'lego creator', 'lego architecture'
            ],
            'sporting_goods': [
                'golf clubs', 'bike', 'kayak', 'ski equipment',
                'exercise equipment', 'camping gear', 'fishing gear'
            ],
            'baby_equipment': [
                'stroller', 'car seat', 'crib', 'high chair',
                'baby monitor', 'breast pump', 'baby carrier'
            ],
            'electronics': [
                'laptop', 'ipad', 'tablet', 'smart watch',
                'airpods', 'gaming console', 'monitor'
            ],
            'photography': [
                'canon camera', 'nikon camera', 'lens',
                'tripod', 'flash', 'camera bag', 'drone'
            ],
            'tools': [
                'dewalt', 'milwaukee tools', 'power drill',
                'saw', 'tool set', 'air compressor', 'impact driver'
            ]
        }
        
        return keyword_map.get(category, [category])


class PriceValidator:
    """
    Validates pricing using APIs like Keepa, CamelCamelCamel, etc.
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.keepa_key = os.getenv('KEEPA_API_KEY')
        
    async def get_amazon_price(self, asin: str) -> Optional[Dict]:
        """Get current Amazon price and history using Keepa"""
        
        if not self.keepa_key:
            logger.warning("Keepa API key not configured")
            return None
        
        try:
            import keepa
            
            api = keepa.Keepa(self.keepa_key)
            
            # Request product info
            products = api.query(asin)
            
            if products and len(products) > 0:
                product = products[0]
                
                # Extract pricing data
                current_price = product.get('stats', {}).get('current', [None, None, None])[0]
                avg_30day = product.get('stats', {}).get('avg30', [None, None, None])[0]
                sales_rank = product.get('stats', {}).get('salesRank', None)
                
                # Convert Keepa prices (stored as cents)
                if current_price:
                    current_price = current_price / 100
                if avg_30day:
                    avg_30day = avg_30day / 100
                
                return {
                    'asin': asin,
                    'current_price': current_price,
                    'avg_30day_price': avg_30day,
                    'sales_rank': sales_rank,
                    'in_stock': current_price is not None,
                    'source': 'keepa'
                }
                
        except Exception as e:
            logger.error(f"Keepa API error for ASIN {asin}: {e}")
        
        return None
    
    async def get_book_prices(self, isbn: str) -> Optional[Dict]:
        """Get book buyback prices from BookScouter"""
        
        api_key = os.getenv('BOOKSCOUTER_API_KEY')
        if not api_key:
            logger.warning("BookScouter API key not configured")
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                url = f"https://bookscouter.com/api/v3/prices"
                params = {
                    'api_key': api_key,
                    'isbn': isbn
                }
                
                response = await client.get(url, params=params, timeout=15)
                data = response.json()
                
                # Get highest buyback price
                prices = data.get('prices', [])
                if prices:
                    highest = max(prices, key=lambda x: x.get('price', 0))
                    
                    return {
                        'isbn': isbn,
                        'highest_buyback': highest.get('price'),
                        'vendor': highest.get('vendor_name'),
                        'total_vendors': len(prices),
                        'source': 'bookscouter'
                    }
                    
        except Exception as e:
            logger.error(f"BookScouter API error for ISBN {isbn}: {e}")
        
        return None
    
    async def validate_opportunity(self, 
                                  source_listing: Dict,
                                  category: str) -> Optional[Dict]:
        """
        Validate if a source listing has profitable resale potential
        """
        
        # Extract product identifier
        identifier = self._extract_identifier(source_listing, category)
        
        if not identifier:
            logger.debug("Could not extract product identifier")
            return None
        
        # Get pricing data based on category
        if category == 'books':
            price_data = await self.get_book_prices(identifier)
        else:
            # Try to find ASIN for Amazon
            asin = await self._find_asin(source_listing['title'], category)
            if asin:
                price_data = await self.get_amazon_price(asin)
            else:
                price_data = None
        
        if not price_data:
            return None
        
        # Calculate profitability
        return self._calculate_profitability(source_listing, price_data, category)
    
    def _extract_identifier(self, listing: Dict, category: str) -> Optional[str]:
        """Extract product identifier (ISBN, UPC, etc.) from listing"""
        
        title = listing.get('title', '').lower()
        description = listing.get('description', '').lower()
        
        # ISBN extraction for books
        if category == 'books':
            import re
            isbn_pattern = r'(?:ISBN[-]?(?:13|10)?[:]?[\s]?)?((?:97[89][-]?)?[0-9]{9}[0-9Xx])'
            match = re.search(isbn_pattern, title + ' ' + description)
            if match:
                return match.group(1).replace('-', '')
        
        # UPC extraction
        upc_pattern = r'\b[0-9]{12}\b'
        import re
        match = re.search(upc_pattern, title + ' ' + description)
        if match:
            return match.group(0)
        
        return None
    
    async def _find_asin(self, product_title: str, category: str) -> Optional[str]:
        """Find Amazon ASIN for a product"""
        # This would use Amazon Product Advertising API or scraping
        # Placeholder implementation
        return None
    
    def _calculate_profitability(self, 
                                source: Dict,
                                price_data: Dict,
                                category: str) -> Dict:
        """Calculate profitability metrics"""
        
        source_price = source.get('price', 0)
        target_price = price_data.get('current_price') or price_data.get('highest_buyback', 0)
        
        # Estimate fees (simplified)
        if category == 'books':
            # Amazon FBA fees for books
            fees = 1.80 + (target_price * 0.15)  # Referral fee
        else:
            # General Amazon fees
            fees = target_price * 0.15  # 15% referral
            fees += 3.00  # FBA fulfillment estimate
        
        shipping_estimate = 5.00  # Estimate
        
        total_costs = source_price + fees + shipping_estimate
        profit = target_price - total_costs
        margin = profit / target_price if target_price > 0 else 0
        roi = profit / source_price if source_price > 0 else 0
        
        return {
            'source_price': source_price,
            'target_price': target_price,
            'estimated_fees': fees,
            'estimated_shipping': shipping_estimate,
            'estimated_profit': profit,
            'profit_margin': margin,
            'roi': roi,
            'viable': margin >= 0.20 and profit >= 10  # Min $10 profit, 20% margin
        }

