"""
Redis Caching Strategy for Blazing-Fast Performance
Reduces database load and API calls
"""

import redis
import json
from typing import Optional, Any
from functools import wraps
import hashlib
from loguru import logger
import os


class RedisCache:
    """
    Redis caching layer for frequently accessed data
    """
    
    def __init__(self):
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.default_ttl = 300  # 5 minutes
        
        logger.info("Redis cache initialized")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        
        try:
            ttl = ttl or self.default_ttl
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value, default=str)
            )
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        """Delete key from cache"""
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    def cache_api_response(self, api_name: str, params: Dict, ttl: int = 3600):
        """
        Decorator to cache API responses
        Reduces expensive API calls
        """
        
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                param_str = json.dumps(params, sort_keys=True)
                cache_key = f"api:{api_name}:{hashlib.md5(param_str.encode()).hexdigest()}"
                
                # Check cache
                cached = self.get(cache_key)
                if cached:
                    logger.debug(f"Cache hit for {api_name}")
                    return cached
                
                # Call API
                result = await func(*args, **kwargs)
                
                # Store in cache
                if result:
                    self.set(cache_key, result, ttl)
                
                return result
            
            return wrapper
        return decorator
    
    def cache_price_data(self, product_id: str, marketplace: str, price: float):
        """Cache price data for quick access"""
        
        key = f"price:{marketplace}:{product_id}"
        data = {
            'price': price,
            'cached_at': datetime.utcnow().isoformat()
        }
        
        self.set(key, data, ttl=600)  # 10 minutes
    
    def get_cached_price(self, product_id: str, marketplace: str) -> Optional[float]:
        """Get cached price if available"""
        
        key = f"price:{marketplace}:{product_id}"
        data = self.get(key)
        
        return data.get('price') if data else None
    
    def cache_opportunities(self, category: str, opportunities: List[Dict]):
        """Cache discovered opportunities"""
        
        key = f"opportunities:{category}"
        self.set(key, opportunities, ttl=300)  # 5 minutes
    
    def get_cached_opportunities(self, category: str) -> Optional[List[Dict]]:
        """Get cached opportunities"""
        
        key = f"opportunities:{category}"
        return self.get(key)
    
    def increment_counter(self, counter_name: str) -> int:
        """Increment a counter (for metrics)"""
        
        try:
            return self.redis_client.incr(counter_name)
        except Exception as e:
            logger.error(f"Counter increment error: {e}")
            return 0
    
    def get_counter(self, counter_name: str) -> int:
        """Get counter value"""
        
        try:
            value = self.redis_client.get(counter_name)
            return int(value) if value else 0
        except Exception as e:
            logger.error(f"Counter get error: {e}")
            return 0
    
    def reset_daily_counters(self):
        """Reset daily counters (call at midnight)"""
        
        counters = [
            'daily:opportunities_found',
            'daily:purchases_made',
            'daily:listings_created',
            'daily:sales_completed'
        ]
        
        for counter in counters:
            self.redis_client.delete(counter)
        
        logger.info("Daily counters reset")


class CacheWarmer:
    """
    Proactively warms cache with frequently accessed data
    """
    
    def __init__(self, cache: RedisCache):
        self.cache = cache
    
    async def warm_price_cache(self, popular_products: List[str]):
        """
        Pre-fetch and cache prices for popular products
        """
        
        logger.info(f"Warming cache for {len(popular_products)} products")
        
        # TODO: Fetch prices and store in cache
        # This runs in background to speed up future requests
        
        pass
    
    async def warm_category_cache(self, categories: List[str]):
        """
        Pre-load category data into cache
        """
        
        for category in categories:
            # TODO: Load category configuration
            # TODO: Load recent opportunities
            pass

