"""
API Integrations
Wrappers for all external APIs
"""

import os
from typing import Dict, List, Optional
import httpx
from loguru import logger


class KeepaAPI:
    """Keepa API for Amazon price tracking"""
    
    def __init__(self):
        self.api_key = os.getenv('KEEPA_API_KEY')
        self.base_url = "https://api.keepa.com"
    
    async def get_product(self, asin: str) -> Optional[Dict]:
        """Get product data from Keepa"""
        
        if not self.api_key:
            return None
        
        try:
            import keepa
            api = keepa.Keepa(self.api_key)
            products = api.query(asin)
            
            if products:
                return products[0]
            
        except Exception as e:
            logger.error(f"Keepa API error: {e}")
        
        return None


class BookScouterAPI:
    """BookScouter API for textbook buyback prices"""
    
    def __init__(self):
        self.api_key = os.getenv('BOOKSCOUTER_API_KEY')
        self.base_url = "https://bookscouter.com/api/v3"
    
    async def get_prices(self, isbn: str) -> Optional[List[Dict]]:
        """Get buyback prices for ISBN"""
        
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/prices",
                    params={'api_key': self.api_key, 'isbn': isbn},
                    timeout=15
                )
                
                data = response.json()
                return data.get('prices', [])
                
        except Exception as e:
            logger.error(f"BookScouter API error: {e}")
        
        return None


class TCGPlayerAPI:
    """TCGPlayer API for trading card prices"""
    
    def __init__(self):
        self.api_key = os.getenv('TCGPLAYER_API_KEY')
        self.base_url = "https://api.tcgplayer.com"
    
    async def search_card(self, card_name: str, game: str = 'pokemon') -> Optional[List[Dict]]:
        """Search for card pricing"""
        
        if not self.api_key:
            return None
        
        # TCGPlayer API requires OAuth
        # This is a simplified placeholder
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {'Authorization': f'Bearer {self.api_key}'}
                
                response = await client.get(
                    f"{self.base_url}/catalog/products",
                    params={'name': card_name, 'category': game},
                    headers=headers,
                    timeout=15
                )
                
                return response.json().get('results', [])
                
        except Exception as e:
            logger.error(f"TCGPlayer API error: {e}")
        
        return None


class BuyBotProAPI:
    """BuyBotPro API for Amazon restriction checking"""
    
    def __init__(self):
        self.api_key = os.getenv('BUYBOT_PRO_API_KEY')
    
    async def check_restrictions(self, asin: str) -> Dict:
        """Check if ASIN is restricted to sell"""
        
        if not self.api_key:
            return {'restricted': False, 'checked': False}
        
        try:
            # BuyBotPro API endpoint
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.buybotpro.com/check",
                    params={'api_key': self.api_key, 'asin': asin},
                    timeout=10
                )
                
                data = response.json()
                
                return {
                    'restricted': data.get('restricted', False),
                    'hazmat': data.get('hazmat', False),
                    'gated': data.get('gated', False),
                    'checked': True,
                    'details': data
                }
                
        except Exception as e:
            logger.error(f"BuyBotPro API error: {e}")
            return {'restricted': False, 'checked': False, 'error': str(e)}


class TacticalArbitrageAPI:
    """Tactical Arbitrage API for automated sourcing"""
    
    def __init__(self):
        self.api_key = os.getenv('TACTICAL_ARBITRAGE_API_KEY')
        self.base_url = "https://api.tacticalarbitrage.com"
    
    async def start_scan(self, scan_config: Dict) -> Dict:
        """Start automated product scan"""
        
        if not self.api_key:
            return {'success': False, 'error': 'API key not configured'}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/scans",
                    headers={'Authorization': f'Bearer {self.api_key}'},
                    json=scan_config,
                    timeout=30
                )
                
                result = response.json()
                
                return {
                    'success': True,
                    'scan_id': result.get('scan_id'),
                    'status': result.get('status')
                }
                
        except Exception as e:
            logger.error(f"Tactical Arbitrage API error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_results(self, scan_id: str) -> Optional[List[Dict]]:
        """Get scan results"""
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/scans/{scan_id}/results",
                    headers={'Authorization': f'Bearer {self.api_key}'},
                    timeout=30
                )
                
                return response.json().get('products', [])
                
        except Exception as e:
            logger.error(f"Failed to get scan results: {e}")
        
        return None


class PriceChartingAPI:
    """PriceCharting API for video game and collectibles pricing"""
    
    def __init__(self):
        self.api_key = os.getenv('PRICECHARTING_API_KEY')
        self.base_url = "https://www.pricecharting.com/api"
    
    async def get_price(self, product_name: str, console: Optional[str] = None) -> Optional[Dict]:
        """Get current market price"""
        
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    'api_key': self.api_key,
                    't': 'search',
                    'q': product_name
                }
                
                if console:
                    params['console'] = console
                
                response = await client.get(
                    f"{self.base_url}/product",
                    params=params,
                    timeout=15
                )
                
                data = response.json()
                
                if data.get('products'):
                    product = data['products'][0]
                    
                    return {
                        'product_name': product.get('product-name'),
                        'loose_price': product.get('loose-price'),
                        'cib_price': product.get('cib-price'),  # Complete in box
                        'new_price': product.get('new-price'),
                        'console': product.get('console-name')
                    }
                    
        except Exception as e:
            logger.error(f"PriceCharting API error: {e}")
        
        return None


class ReverbAPI:
    """Reverb API for musical instrument pricing"""
    
    def __init__(self):
        self.api_key = os.getenv('REVERB_API_KEY')
        self.base_url = "https://api.reverb.com/api"
    
    async def search_listings(self, query: str) -> Optional[List[Dict]]:
        """Search Reverb listings"""
        
        if not self.api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Accept': 'application/hal+json'
                }
                
                response = await client.get(
                    f"{self.base_url}/listings",
                    params={'query': query},
                    headers=headers,
                    timeout=15
                )
                
                data = response.json()
                return data.get('listings', [])
                
        except Exception as e:
            logger.error(f"Reverb API error: {e}")
        
        return None
    
    async def get_price_guide(self, make: str, model: str) -> Optional[Dict]:
        """Get price guide for instrument"""
        
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Accept': 'application/hal+json'
                }
                
                response = await client.get(
                    f"{self.base_url}/priceguide",
                    params={'make': make, 'model': model},
                    headers=headers,
                    timeout=15
                )
                
                return response.json()
                
        except Exception as e:
            logger.error(f"Reverb price guide error: {e}")
        
        return None


class BrickLinkAPI:
    """BrickLink API for LEGO pricing"""
    
    def __init__(self):
        self.api_key = os.getenv('BRICKLINK_API_KEY')
        self.base_url = "https://api.bricklink.com/api/store/v1"
    
    async def get_set_price(self, set_number: str) -> Optional[Dict]:
        """Get LEGO set pricing"""
        
        if not self.api_key:
            return None
        
        # BrickLink uses OAuth 1.0
        # This is a simplified placeholder
        
        try:
            logger.info(f"Fetching BrickLink price for set {set_number}")
            
            # Implementation requires OAuth signing
            # Return placeholder
            
            return {
                'set_number': set_number,
                'avg_price': None,
                'checked': False
            }
            
        except Exception as e:
            logger.error(f"BrickLink API error: {e}")
        
        return None


class APIManager:
    """Central manager for all API integrations"""
    
    def __init__(self):
        self.keepa = KeepaAPI()
        self.bookscouter = BookScouterAPI()
        self.tcgplayer = TCGPlayerAPI()
        self.buybot = BuyBotProAPI()
        self.tactical_arbitrage = TacticalArbitrageAPI()
        self.pricecharting = PriceChartingAPI()
        self.reverb = ReverbAPI()
        self.bricklink = BrickLinkAPI()
    
    async def get_price_data(self, product: Dict, category: str) -> Optional[Dict]:
        """Get pricing data from appropriate API based on category"""
        
        if category == 'books':
            isbn = product.get('isbn')
            if isbn:
                return await self.bookscouter.get_prices(isbn)
        
        elif category == 'trading_cards':
            card_name = product.get('name')
            if card_name:
                return await self.tcgplayer.search_card(card_name)
        
        elif category == 'video_games':
            game_name = product.get('name')
            if game_name:
                return await self.pricecharting.get_price(game_name)
        
        elif category == 'musical_instruments':
            make = product.get('make')
            model = product.get('model')
            if make and model:
                return await self.reverb.get_price_guide(make, model)
        
        elif category == 'lego':
            set_number = product.get('set_number')
            if set_number:
                return await self.bricklink.get_set_price(set_number)
        
        # Default to Amazon via Keepa
        asin = product.get('asin')
        if asin:
            return await self.keepa.get_product(asin)
        
        return None

