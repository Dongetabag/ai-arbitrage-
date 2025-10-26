"""
MongoDB Integration for High-Volume Price Data
NoSQL database for rapid inserts and flexible schema
Stores 144,000 data points daily from 500 sites
"""

from pymongo import MongoClient, IndexModel, ASCENDING, DESCENDING
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
import os


class MongoDBManager:
    """
    MongoDB for high-volume, unstructured data
    Perfect for price scrapes with rapid inserts
    """
    
    def __init__(self):
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['arbitrage_db']
        
        # Collections
        self.price_scrapes = self.db['price_scrapes']
        self.raw_listings = self.db['raw_listings']
        self.market_snapshots = self.db['market_snapshots']
        
        # Create indexes
        self._create_indexes()
        
        logger.info("MongoDB initialized")
    
    def _create_indexes(self):
        """Create indexes for fast queries"""
        
        # Price scrapes indexes
        self.price_scrapes.create_index([
            ('product_id', ASCENDING),
            ('marketplace', ASCENDING),
            ('scraped_at', DESCENDING)
        ])
        
        self.price_scrapes.create_index([
            ('scraped_at', DESCENDING)
        ])
        
        # Raw listings indexes
        self.raw_listings.create_index([
            ('discovered_at', DESCENDING)
        ])
        
        self.raw_listings.create_index([
            ('category', ASCENDING),
            ('price', ASCENDING)
        ])
        
        logger.info("MongoDB indexes created")
    
    async def store_price_scrape(self, scrape_data: Dict):
        """
        Store individual price scrape
        
        Optimized for high-volume inserts (144,000/day)
        """
        
        document = {
            'product_id': scrape_data.get('product_id'),
            'marketplace': scrape_data.get('marketplace'),
            'price': scrape_data.get('price'),
            'in_stock': scrape_data.get('in_stock', True),
            'sales_rank': scrape_data.get('sales_rank'),
            'seller_name': scrape_data.get('seller'),
            'condition': scrape_data.get('condition'),
            'scraped_at': datetime.utcnow(),
            'metadata': scrape_data.get('metadata', {})
        }
        
        try:
            self.price_scrapes.insert_one(document)
        except Exception as e:
            logger.error(f"Failed to store price scrape: {e}")
    
    async def store_raw_listing(self, listing: Dict):
        """Store raw marketplace listing"""
        
        document = {
            'title': listing.get('title'),
            'price': listing.get('price'),
            'marketplace': listing.get('marketplace'),
            'url': listing.get('url'),
            'category': listing.get('category'),
            'description': listing.get('description'),
            'images': listing.get('images', []),
            'seller_info': listing.get('seller_info', {}),
            'location': listing.get('location'),
            'discovered_at': datetime.utcnow(),
            'processed': False
        }
        
        try:
            result = self.raw_listings.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to store listing: {e}")
            return None
    
    async def bulk_insert_scrapes(self, scrapes: List[Dict]):
        """
        Bulk insert for efficiency
        Use when processing large batches
        """
        
        if not scrapes:
            return
        
        documents = []
        for scrape in scrapes:
            documents.append({
                'product_id': scrape.get('product_id'),
                'marketplace': scrape.get('marketplace'),
                'price': scrape.get('price'),
                'scraped_at': datetime.utcnow(),
                'metadata': scrape.get('metadata', {})
            })
        
        try:
            result = self.price_scrapes.insert_many(documents, ordered=False)
            logger.info(f"Bulk inserted {len(result.inserted_ids)} price scrapes")
        except Exception as e:
            logger.error(f"Bulk insert failed: {e}")
    
    async def get_price_history(self,
                               product_id: str,
                               marketplace: str,
                               days: int = 30) -> List[Dict]:
        """
        Get price history for a product
        """
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        cursor = self.price_scrapes.find({
            'product_id': product_id,
            'marketplace': marketplace,
            'scraped_at': {'$gte': cutoff_date}
        }).sort('scraped_at', DESCENDING)
        
        return list(cursor)
    
    async def get_unprocessed_listings(self, limit: int = 100) -> List[Dict]:
        """
        Get raw listings that haven't been processed yet
        """
        
        cursor = self.raw_listings.find({
            'processed': False
        }).sort('discovered_at', DESCENDING).limit(limit)
        
        return list(cursor)
    
    async def mark_listing_processed(self, listing_id: str):
        """Mark listing as processed"""
        
        from bson import ObjectId
        
        self.raw_listings.update_one(
            {'_id': ObjectId(listing_id)},
            {'$set': {'processed': True, 'processed_at': datetime.utcnow()}}
        )
    
    async def store_market_snapshot(self, category: str, data: Dict):
        """
        Store market snapshot for analysis
        
        Captures: avg prices, total listings, trend direction
        """
        
        document = {
            'category': category,
            'avg_price': data.get('avg_price'),
            'median_price': data.get('median_price'),
            'total_listings': data.get('total_listings'),
            'marketplaces': data.get('marketplaces', {}),
            'snapshot_at': datetime.utcnow()
        }
        
        self.market_snapshots.insert_one(document)
    
    async def get_trending_products(self, category: str, limit: int = 20) -> List[Dict]:
        """
        Get trending products based on listing frequency
        """
        
        # Aggregate listings from last 24 hours
        pipeline = [
            {
                '$match': {
                    'category': category,
                    'discovered_at': {'$gte': datetime.utcnow() - timedelta(days=1)}
                }
            },
            {
                '$group': {
                    '_id': '$title',
                    'count': {'$sum': 1},
                    'avg_price': {'$avg': '$price'},
                    'marketplaces': {'$addToSet': '$marketplace'}
                }
            },
            {
                '$sort': {'count': -1}
            },
            {
                '$limit': limit
            }
        ]
        
        results = list(self.market_snapshots.aggregate(pipeline))
        
        return results
    
    async def cleanup_old_data(self, days_to_keep: int = 90):
        """
        Remove old price scrapes to manage storage
        """
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        result = self.price_scrapes.delete_many({
            'scraped_at': {'$lt': cutoff_date}
        })
        
        logger.info(f"Cleaned up {result.deleted_count} old price scrapes")

