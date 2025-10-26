"""
Playwright Integration for Dynamic Content Scraping
Handles modern SPAs (React/Vue) like Facebook Marketplace, OfferUp
"""

from playwright.async_api import async_playwright, Page, Browser
from typing import List, Dict
from loguru import logger
import asyncio
from datetime import datetime


class PlaywrightScraper:
    """
    High-performance scraper for JavaScript-heavy sites
    Preferred over Selenium for modern automation
    """
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Browser = None
    
    async def initialize(self):
        """Initialize Playwright browser"""
        
        playwright = await async_playwright().start()
        
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-dev-shm-usage'
            ]
        )
        
        logger.info("Playwright browser initialized")
    
    async def scrape_facebook_marketplace(self,
                                         keyword: str,
                                         location: str,
                                         max_results: int = 50) -> List[Dict]:
        """
        Scrape Facebook Marketplace with full JavaScript rendering
        """
        
        if not self.browser:
            await self.initialize()
        
        logger.info(f"Scraping Facebook Marketplace for '{keyword}' in {location}")
        
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        
        page = await context.new_page()
        
        try:
            # Navigate to marketplace
            # Note: This requires Facebook authentication in production
            search_url = f"https://www.facebook.com/marketplace/category/search/?query={keyword}"
            
            await page.goto(search_url, wait_until='networkidle')
            
            # Wait for listings to load
            await page.wait_for_selector('[data-testid="marketplace-product-card"]', timeout=10000)
            
            # Scroll to load more results
            for _ in range(3):
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)
            
            # Extract listings
            listings = await page.query_selector_all('[data-testid="marketplace-product-card"]')
            
            results = []
            
            for listing in listings[:max_results]:
                try:
                    # Extract data
                    title_elem = await listing.query_selector('span')
                    price_elem = await listing.query_selector('[class*="price"]')
                    link_elem = await listing.query_selector('a')
                    
                    title = await title_elem.inner_text() if title_elem else ''
                    price_text = await price_elem.inner_text() if price_elem else '0'
                    url = await link_elem.get_attribute('href') if link_elem else ''
                    
                    # Parse price
                    price = self._parse_price(price_text)
                    
                    if title and price > 0:
                        results.append({
                            'marketplace': 'facebook_marketplace',
                            'title': title,
                            'price': price,
                            'url': f"https://facebook.com{url}" if url.startswith('/') else url,
                            'location': location,
                            'discovered_at': datetime.utcnow().isoformat(),
                            'scraped_with': 'playwright'
                        })
                
                except Exception as e:
                    logger.debug(f"Error parsing listing: {e}")
                    continue
            
            logger.info(f"Found {len(results)} listings on Facebook Marketplace")
            
            return results
            
        except Exception as e:
            logger.error(f"Facebook scraping error: {e}")
            return []
        
        finally:
            await page.close()
            await context.close()
    
    async def scrape_offerup(self, keyword: str, zipcode: str, max_results: int = 50) -> List[Dict]:
        """
        Scrape OfferUp with JavaScript rendering
        """
        
        if not self.browser:
            await self.initialize()
        
        logger.info(f"Scraping OfferUp for '{keyword}'")
        
        context = await self.browser.new_context()
        page = await context.new_page()
        
        try:
            # OfferUp search URL
            url = f"https://offerup.com/search/?q={keyword}"
            
            await page.goto(url, wait_until='networkidle')
            
            # Wait for results
            await page.wait_for_selector('[data-testid="listing-card"]', timeout=10000)
            
            # Scroll to load more
            for _ in range(3):
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                await asyncio.sleep(1)
            
            # Extract listings
            listings = await page.query_selector_all('[data-testid="listing-card"]')
            
            results = []
            
            for listing in listings[:max_results]:
                try:
                    title = await listing.query_selector_text('h3')
                    price_text = await listing.query_selector_text('[data-testid="price"]')
                    link = await listing.query_selector_attribute('a', 'href')
                    
                    price = self._parse_price(price_text)
                    
                    if title and price > 0:
                        results.append({
                            'marketplace': 'offerup',
                            'title': title,
                            'price': price,
                            'url': f"https://offerup.com{link}" if link.startswith('/') else link,
                            'discovered_at': datetime.utcnow().isoformat(),
                            'scraped_with': 'playwright'
                        })
                
                except Exception as e:
                    logger.debug(f"Error parsing OfferUp listing: {e}")
                    continue
            
            logger.info(f"Found {len(results)} listings on OfferUp")
            
            return results
            
        except Exception as e:
            logger.error(f"OfferUp scraping error: {e}")
            return []
        
        finally:
            await page.close()
            await context.close()
    
    async def automate_purchase(self,
                               url: str,
                               seller_contact: Dict,
                               payment_info: Dict) -> Dict:
        """
        Automate purchase checkout process
        Mimics human actions: login, navigate, add to cart, checkout
        """
        
        if not self.browser:
            await self.initialize()
        
        logger.info(f"Automating purchase for {url}")
        
        context = await self.browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to product
            await page.goto(url, wait_until='networkidle')
            
            # Click "Buy Now" or "Add to Cart" button
            buy_button = await page.query_selector('button:has-text("Buy Now"), button:has-text("Add to Cart")')
            
            if buy_button:
                await buy_button.click()
                await page.wait_for_load_state('networkidle')
                
                # Fill checkout form if present
                # This varies greatly by platform
                
                logger.info("Purchase automation: Checkout page reached")
                
                # In production, handle payment forms carefully
                # For now, return manual intervention needed
                
                return {
                    'success': True,
                    'status': 'checkout_ready',
                    'requires_manual': True,
                    'message': 'Navigated to checkout - manual payment required'
                }
            else:
                return {
                    'success': False,
                    'error': 'Buy button not found'
                }
        
        except Exception as e:
            logger.error(f"Purchase automation error: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        
        finally:
            await page.close()
            await context.close()
    
    def _parse_price(self, price_text: str) -> float:
        """Extract numeric price"""
        import re
        
        if not price_text:
            return 0.0
        
        cleaned = re.sub(r'[$,]', '', price_text)
        match = re.search(r'\d+\.?\d*', cleaned)
        
        return float(match.group()) if match else 0.0
    
    async def query_selector_text(self, element, selector: str) -> str:
        """Helper to get text from selector"""
        elem = await element.query_selector(selector)
        return await elem.inner_text() if elem else ''
    
    async def query_selector_attribute(self, element, selector: str, attr: str) -> str:
        """Helper to get attribute from selector"""
        elem = await element.query_selector(selector)
        return await elem.get_attribute(attr) if elem else ''
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
            logger.info("Playwright browser closed")

