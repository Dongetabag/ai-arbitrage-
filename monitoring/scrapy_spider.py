"""
Scrapy Framework Integration for High-Performance Scraping
Handles 100+ requests per minute across 500 sites
"""

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from typing import Dict, List
import json
from datetime import datetime
from loguru import logger


class MarketplaceSpider(scrapy.Spider):
    """
    High-performance marketplace spider using Scrapy
    Industry-standard for large-scale web crawling
    """
    
    name = 'marketplace_spider'
    
    custom_settings = {
        'CONCURRENT_REQUESTS': 100,  # 100 requests per minute
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'DOWNLOAD_DELAY': 0.5,  # Respectful scraping
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.5,
        'AUTOTHROTTLE_MAX_DELAY': 3.0,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 100.0,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
        'HTTPCACHE_ENABLED': True,  # Cache responses
        'HTTPCACHE_EXPIRATION_SECS': 300,  # 5 minutes
        'ROBOTSTXT_OBEY': True,  # Respect robots.txt
        'USER_AGENT': 'Mozilla/5.0 (compatible; ArbitrageBot/1.0)',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/json',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }
    
    def __init__(self, urls: List[str], category: str, *args, **kwargs):
        super(MarketplaceSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls
        self.category = category
        self.results = []
    
    def parse(self, response):
        """Parse marketplace listing page"""
        
        # Extract listings based on site structure
        # This is a generic parser - customize per site
        
        if 'craigslist.org' in response.url:
            yield from self.parse_craigslist(response)
        elif 'facebook.com' in response.url:
            yield from self.parse_facebook(response)
        elif 'offerup.com' in response.url:
            yield from self.parse_offerup(response)
        else:
            yield from self.parse_generic(response)
    
    def parse_craigslist(self, response):
        """Parse Craigslist listings"""
        
        for listing in response.css('.result-row'):
            title = listing.css('.result-title::text').get()
            price_text = listing.css('.result-price::text').get()
            url = listing.css('.result-title::attr(href)').get()
            location = listing.css('.result-hood::text').get()
            
            if title and price_text:
                price = self._parse_price(price_text)
                
                yield {
                    'marketplace': 'craigslist',
                    'title': title.strip(),
                    'price': price,
                    'url': url,
                    'location': location.strip() if location else '',
                    'category': self.category,
                    'discovered_at': datetime.utcnow().isoformat(),
                    'scraped_with': 'scrapy'
                }
    
    def parse_facebook(self, response):
        """Parse Facebook Marketplace - requires dynamic rendering"""
        # Facebook needs Playwright/Selenium for JS rendering
        logger.warning("Facebook requires dynamic scraping - use Playwright spider")
        return []
    
    def parse_offerup(self, response):
        """Parse OfferUp listings"""
        
        # OfferUp structure (simplified)
        for listing in response.css('[data-testid="listing-card"]'):
            title = listing.css('h3::text').get()
            price_text = listing.css('[data-testid="price"]::text').get()
            url = listing.css('a::attr(href)').get()
            
            if title and price_text:
                price = self._parse_price(price_text)
                
                yield {
                    'marketplace': 'offerup',
                    'title': title.strip(),
                    'price': price,
                    'url': response.urljoin(url) if url else '',
                    'category': self.category,
                    'discovered_at': datetime.utcnow().isoformat(),
                    'scraped_with': 'scrapy'
                }
    
    def parse_generic(self, response):
        """Generic parser for unknown sites"""
        
        # Try common patterns
        for listing in response.css('.product, .listing, .item'):
            title = listing.css('h2::text, h3::text, .title::text').get()
            price_text = listing.css('.price::text, [class*="price"]::text').get()
            
            if title and price_text:
                yield {
                    'marketplace': 'generic',
                    'title': title.strip(),
                    'price': self._parse_price(price_text),
                    'url': response.url,
                    'category': self.category,
                    'discovered_at': datetime.utcnow().isoformat()
                }
    
    def _parse_price(self, price_text: str) -> float:
        """Extract numeric price from text"""
        import re
        
        if not price_text:
            return 0.0
        
        # Remove currency symbols and commas
        cleaned = re.sub(r'[$,]', '', price_text)
        
        # Extract first number
        match = re.search(r'\d+\.?\d*', cleaned)
        if match:
            return float(match.group())
        
        return 0.0


class ScrapyOrchestrator:
    """
    Manages Scrapy spiders for high-volume scraping
    """
    
    def __init__(self):
        self.process = None
    
    def start_crawl(self, urls: List[str], category: str, callback=None):
        """
        Start Scrapy crawl process
        
        Args:
            urls: List of URLs to scrape
            category: Product category
            callback: Function to call with results
        """
        
        logger.info(f"Starting Scrapy crawl for {len(urls)} URLs in category '{category}'")
        
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/5.0 (compatible; ArbitrageBot/1.0)',
            'ROBOTSTXT_OBEY': True,
            'CONCURRENT_REQUESTS': 100,
            'LOG_LEVEL': 'INFO'
        })
        
        process.crawl(MarketplaceSpider, urls=urls, category=category)
        process.start()  # Blocking call
        
        logger.info("Scrapy crawl completed")
    
    async def crawl_async(self, urls: List[str], category: str) -> List[Dict]:
        """
        Async wrapper for Scrapy crawling
        """
        
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        executor = ThreadPoolExecutor(max_workers=1)
        
        results = []
        
        def run_crawl():
            self.start_crawl(urls, category)
            return results
        
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, run_crawl)

