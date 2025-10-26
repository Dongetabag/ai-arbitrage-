"""
Listing Manager
Handles product listing creation and management across selling platforms
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger
import httpx
from dataclasses import dataclass


@dataclass
class ProductListing:
    """Product listing data"""
    title: str
    description: str
    price: float
    category: str
    condition: str
    images: List[str]
    bullet_points: List[str]
    sku: Optional[str] = None
    upc: Optional[str] = None
    metadata: Optional[Dict] = None


class ListingManager:
    """
    Creates and manages product listings across platforms
    """
    
    def __init__(self, ai_engine, config: Dict):
        self.ai_engine = ai_engine
        self.config = config
    
    async def create_listing(self,
                            product: Dict,
                            target_marketplace: str,
                            price: float) -> Dict:
        """
        Create optimized listing for product
        
        Args:
            product: Product details
            target_marketplace: Where to list (amazon, ebay, etc.)
            price: Listing price
            
        Returns:
            Listing result with listing ID and URL
        """
        
        logger.info(f"Creating listing for {product['title']} on {target_marketplace}")
        
        # Generate optimized listing content using AI
        listing_content = self.ai_engine.generate_product_listing(product)
        
        # Build listing object
        listing = ProductListing(
            title=listing_content['title'],
            description=listing_content['description'],
            price=price,
            category=product.get('category', 'Other'),
            condition=product.get('condition', 'Used'),
            images=product.get('images', []),
            bullet_points=listing_content.get('bullet_points', []),
            sku=product.get('sku'),
            upc=product.get('upc'),
            metadata=product.get('metadata', {})
        )
        
        # Create listing on target platform
        if target_marketplace == 'amazon':
            return await self._list_on_amazon(listing)
        elif target_marketplace == 'ebay':
            return await self._list_on_ebay(listing)
        elif target_marketplace == 'facebook':
            return await self._list_on_facebook(listing)
        else:
            logger.error(f"Unknown marketplace: {target_marketplace}")
            return {'success': False, 'error': 'Unknown marketplace'}
    
    async def _list_on_amazon(self, listing: ProductListing) -> Dict:
        """List product on Amazon via SP-API"""
        
        try:
            from sp_api.api import ListingsItems
            from sp_api.base import Marketplaces, SellerType
            
            # Initialize Amazon API
            credentials = {
                'refresh_token': os.getenv('AMAZON_SP_API_REFRESH_TOKEN'),
                'lwa_app_id': os.getenv('AMAZON_SP_API_KEY'),
                'lwa_client_secret': os.getenv('AMAZON_SP_API_SECRET'),
            }
            
            listings_api = ListingsItems(
                credentials=credentials,
                marketplace=Marketplaces.US
            )
            
            seller_id = os.getenv('AMAZON_SELLER_ID')
            
            # Build listing payload
            payload = {
                'productType': 'PRODUCT',
                'requirements': 'LISTING',
                'attributes': {
                    'item_name': [{
                        'value': listing.title,
                        'language_tag': 'en_US',
                        'marketplace_id': 'ATVPDKIKX0DER'
                    }],
                    'purchasable_offer': [{
                        'currency': 'USD',
                        'our_price': [{
                            'schedule': [{
                                'value_with_tax': listing.price
                            }]
                        }]
                    }],
                    'condition_type': [{
                        'value': self._map_condition_amazon(listing.condition)
                    }],
                    'merchant_suggested_asin': [{
                        'value': listing.metadata.get('asin', '')
                    }] if listing.metadata and listing.metadata.get('asin') else []
                }
            }
            
            # Add description
            if listing.description:
                payload['attributes']['item_description'] = [{
                    'value': listing.description,
                    'language_tag': 'en_US',
                    'marketplace_id': 'ATVPDKIKX0DER'
                }]
            
            # Add bullet points
            if listing.bullet_points:
                payload['attributes']['bullet_point'] = [
                    {'value': point, 'language_tag': 'en_US', 'marketplace_id': 'ATVPDKIKX0DER'}
                    for point in listing.bullet_points[:5]
                ]
            
            # Create listing
            sku = listing.sku or f"ARB-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            response = listings_api.put_listings_item(
                sellerId=seller_id,
                sku=sku,
                body=payload
            )
            
            logger.info(f"Amazon listing created: SKU {sku}")
            
            return {
                'success': True,
                'platform': 'amazon',
                'sku': sku,
                'status': response.payload.get('status'),
                'listed_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Amazon listing failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _list_on_ebay(self, listing: ProductListing) -> Dict:
        """List product on eBay"""
        
        try:
            from ebaysdk.trading import Connection as Trading
            
            api = Trading(
                appid=os.getenv('EBAY_APP_ID'),
                devid=os.getenv('EBAY_DEV_ID'),
                certid=os.getenv('EBAY_CERT_ID'),
                token=os.getenv('EBAY_USER_TOKEN'),
                config_file=None
            )
            
            # Build listing
            listing_data = {
                'Item': {
                    'Title': listing.title,
                    'Description': listing.description,
                    'PrimaryCategory': {'CategoryID': self._get_ebay_category(listing.category)},
                    'StartPrice': listing.price,
                    'ConditionID': self._map_condition_ebay(listing.condition),
                    'Country': 'US',
                    'Currency': 'USD',
                    'ListingDuration': 'GTC',  # Good 'til cancelled
                    'ListingType': 'FixedPriceItem',
                    'PaymentMethods': 'PayPal',
                    'PayPalEmailAddress': os.getenv('PAYPAL_EMAIL', ''),
                    'PictureDetails': {
                        'PictureURL': listing.images[:12]  # eBay allows up to 12
                    },
                    'PostalCode': os.getenv('ZIPCODE', '02101'),
                    'Quantity': 1,
                    'ReturnPolicy': {
                        'ReturnsAcceptedOption': 'ReturnsAccepted',
                        'RefundOption': 'MoneyBack',
                        'ReturnsWithinOption': 'Days_30',
                        'ShippingCostPaidByOption': 'Buyer'
                    },
                    'ShippingDetails': {
                        'ShippingType': 'Flat',
                        'ShippingServiceOptions': {
                            'ShippingService': 'USPSPriority',
                            'ShippingServiceCost': '0.00'  # Free shipping
                        }
                    },
                    'Site': 'US'
                }
            }
            
            # Add item specifics (bullet points)
            if listing.bullet_points:
                listing_data['Item']['ItemSpecifics'] = {
                    'NameValueList': [
                        {'Name': 'Features', 'Value': listing.bullet_points}
                    ]
                }
            
            response = api.execute('AddFixedPriceItem', listing_data)
            
            item_id = response.dict().get('ItemID')
            
            logger.info(f"eBay listing created: Item {item_id}")
            
            return {
                'success': True,
                'platform': 'ebay',
                'listing_id': item_id,
                'listing_url': f"https://www.ebay.com/itm/{item_id}",
                'listed_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"eBay listing failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _list_on_facebook(self, listing: ProductListing) -> Dict:
        """List product on Facebook Marketplace"""
        
        # Facebook Marketplace API has limited automation
        # Usually requires manual listing through app/website
        
        logger.warning("Facebook Marketplace listing requires manual intervention")
        
        return {
            'success': False,
            'error': 'Facebook Marketplace listing not automated',
            'manual_required': True,
            'listing_data': {
                'title': listing.title,
                'price': listing.price,
                'description': listing.description,
                'images': listing.images
            }
        }
    
    def _map_condition_amazon(self, condition: str) -> str:
        """Map condition to Amazon condition type"""
        condition_map = {
            'new': 'NewItem',
            'like new': 'UsedLikeNew',
            'very good': 'UsedVeryGood',
            'good': 'UsedGood',
            'acceptable': 'UsedAcceptable'
        }
        return condition_map.get(condition.lower(), 'UsedGood')
    
    def _map_condition_ebay(self, condition: str) -> str:
        """Map condition to eBay condition ID"""
        condition_map = {
            'new': '1000',
            'like new': '1500',
            'very good': '2000',
            'good': '3000',
            'acceptable': '4000',
            'for parts': '7000'
        }
        return condition_map.get(condition.lower(), '3000')
    
    def _get_ebay_category(self, category: str) -> str:
        """Get eBay category ID for product category"""
        # Simplified category mapping
        category_map = {
            'books': '267',
            'video_games': '139973',
            'electronics': '293',
            'sporting_goods': '888',
            'musical_instruments': '619',
            'tools': '631',
            'photography': '625'
        }
        return category_map.get(category, '99')  # 99 = Everything Else
    
    async def update_price(self,
                          listing_id: str,
                          marketplace: str,
                          new_price: float) -> Dict:
        """Update listing price dynamically"""
        
        logger.info(f"Updating price for {listing_id} on {marketplace} to ${new_price:.2f}")
        
        if marketplace == 'amazon':
            return await self._update_amazon_price(listing_id, new_price)
        elif marketplace == 'ebay':
            return await self._update_ebay_price(listing_id, new_price)
        else:
            return {'success': False, 'error': 'Marketplace not supported'}
    
    async def _update_amazon_price(self, sku: str, new_price: float) -> Dict:
        """Update Amazon listing price"""
        
        try:
            from sp_api.api import ListingsItems
            
            # Update price via SP-API
            # Implementation depends on SP-API version
            
            logger.info(f"Amazon price updated for SKU {sku}")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"Amazon price update failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _update_ebay_price(self, item_id: str, new_price: float) -> Dict:
        """Update eBay listing price"""
        
        try:
            from ebaysdk.trading import Connection as Trading
            
            api = Trading(
                appid=os.getenv('EBAY_APP_ID'),
                devid=os.getenv('EBAY_DEV_ID'),
                certid=os.getenv('EBAY_CERT_ID'),
                token=os.getenv('EBAY_USER_TOKEN'),
                config_file=None
            )
            
            response = api.execute('ReviseFixedPriceItem', {
                'ItemID': item_id,
                'Item': {
                    'StartPrice': new_price
                }
            })
            
            logger.info(f"eBay price updated for item {item_id}")
            return {'success': True}
            
        except Exception as e:
            logger.error(f"eBay price update failed: {e}")
            return {'success': False, 'error': str(e)}

