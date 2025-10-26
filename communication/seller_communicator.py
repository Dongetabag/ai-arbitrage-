"""
Seller Communication Module
Handles messaging, negotiation, and deal closing with sellers
"""

import os
from datetime import datetime
from typing import Dict, Optional, List
from twilio.rest import Client as TwilioClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from loguru import logger
import httpx
from bs4 import BeautifulSoup


class SellerCommunicator:
    """
    Manages all communication with sellers across platforms
    """
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Initialize communication channels
        self.twilio_client = self._init_twilio()
        self.sendgrid_client = self._init_sendgrid()
        
    def _init_twilio(self) -> Optional[TwilioClient]:
        """Initialize Twilio for SMS"""
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if account_sid and auth_token:
            return TwilioClient(account_sid, auth_token)
        return None
    
    def _init_sendgrid(self) -> Optional[SendGridAPIClient]:
        """Initialize SendGrid for email"""
        api_key = os.getenv('SENDGRID_API_KEY')
        
        if api_key:
            return SendGridAPIClient(api_key)
        return None
    
    async def contact_seller(self, 
                            opportunity: Dict,
                            message: str,
                            method: str = 'auto') -> Dict:
        """
        Contact seller through appropriate channel
        
        Args:
            opportunity: Opportunity dict with seller info
            message: Message to send
            method: 'sms', 'email', 'marketplace', or 'auto'
            
        Returns:
            Result dict with success status and details
        """
        
        seller_contact = opportunity.get('seller_contact', '')
        marketplace = opportunity.get('source_marketplace', '')
        
        # Determine best contact method
        if method == 'auto':
            method = self._determine_contact_method(seller_contact, marketplace)
        
        logger.info(f"Contacting seller via {method}")
        
        if method == 'sms':
            return await self._send_sms(seller_contact, message)
        elif method == 'email':
            return await self._send_email(seller_contact, message, opportunity)
        elif method == 'marketplace':
            return await self._send_marketplace_message(marketplace, opportunity, message)
        else:
            logger.error(f"Unknown contact method: {method}")
            return {'success': False, 'error': 'Invalid contact method'}
    
    def _determine_contact_method(self, contact: str, marketplace: str) -> str:
        """Determine best method to contact seller"""
        
        # Check if it's a phone number
        if contact and (contact.startswith('+') or len(contact) == 10):
            return 'sms'
        
        # Check if it's an email
        if contact and '@' in contact:
            return 'email'
        
        # Default to marketplace messaging
        return 'marketplace'
    
    async def _send_sms(self, phone: str, message: str) -> Dict:
        """Send SMS via Twilio"""
        
        if not self.twilio_client:
            return {'success': False, 'error': 'Twilio not configured'}
        
        try:
            from_number = os.getenv('TWILIO_PHONE_NUMBER')
            
            # Format phone number
            if not phone.startswith('+'):
                phone = f"+1{phone}"
            
            message_obj = self.twilio_client.messages.create(
                body=message,
                from_=from_number,
                to=phone
            )
            
            logger.info(f"SMS sent successfully: {message_obj.sid}")
            
            return {
                'success': True,
                'message_id': message_obj.sid,
                'method': 'sms',
                'sent_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"SMS send failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _send_email(self, email: str, message: str, opportunity: Dict) -> Dict:
        """Send email via SendGrid"""
        
        if not self.sendgrid_client:
            return {'success': False, 'error': 'SendGrid not configured'}
        
        try:
            from_email = os.getenv('NOTIFICATION_EMAIL', 'noreply@arbitrage.com')
            product_title = opportunity.get('product_title', 'Product')
            
            mail = Mail(
                from_email=from_email,
                to_emails=email,
                subject=f"Interested in your {product_title}",
                plain_text_content=message
            )
            
            response = self.sendgrid_client.send(mail)
            
            logger.info(f"Email sent successfully to {email}")
            
            return {
                'success': True,
                'status_code': response.status_code,
                'method': 'email',
                'sent_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _send_marketplace_message(self, 
                                       marketplace: str,
                                       opportunity: Dict,
                                       message: str) -> Dict:
        """Send message through marketplace platform"""
        
        # Each marketplace has different messaging APIs
        if marketplace == 'facebook_marketplace':
            return await self._send_facebook_message(opportunity, message)
        elif marketplace == 'craigslist':
            return await self._send_craigslist_message(opportunity, message)
        elif marketplace == 'ebay':
            return await self._send_ebay_message(opportunity, message)
        else:
            logger.warning(f"Marketplace messaging not implemented for {marketplace}")
            return {'success': False, 'error': f'Not implemented for {marketplace}'}
    
    async def _send_facebook_message(self, opportunity: Dict, message: str) -> Dict:
        """Send message via Facebook Marketplace"""
        
        # Facebook messaging requires authenticated API access
        # This is a placeholder
        
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        if not access_token:
            return {'success': False, 'error': 'Facebook access token not configured'}
        
        # Implementation would use Facebook Graph API
        logger.info("Facebook messaging: placeholder implementation")
        
        return {
            'success': False,
            'error': 'Facebook messaging requires manual intervention'
        }
    
    async def _send_craigslist_message(self, opportunity: Dict, message: str) -> Dict:
        """Send message via Craigslist relay email"""
        
        # Craigslist uses anonymous relay emails
        # Extract relay email from listing URL
        
        listing_url = opportunity.get('url', '')
        
        # Parse listing to get contact method
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(listing_url, timeout=15)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find contact button/email
                # Craigslist structure varies
                
                logger.info("Craigslist messaging: requires email extraction")
                
        except Exception as e:
            logger.error(f"Craigslist message failed: {e}")
        
        return {
            'success': False,
            'error': 'Craigslist messaging requires manual intervention'
        }
    
    async def _send_ebay_message(self, opportunity: Dict, message: str) -> Dict:
        """Send message via eBay messaging"""
        
        try:
            from ebaysdk.trading import Connection as Trading
            
            api = Trading(
                appid=os.getenv('EBAY_APP_ID'),
                devid=os.getenv('EBAY_DEV_ID'),
                certid=os.getenv('EBAY_CERT_ID'),
                token=os.getenv('EBAY_USER_TOKEN'),
                config_file=None
            )
            
            item_id = opportunity.get('item_id', '')
            
            # Send question to seller
            response = api.execute('AddMemberMessageAAQToPartner', {
                'ItemID': item_id,
                'MemberMessage': {
                    'Subject': 'Question about your item',
                    'Body': message,
                    'QuestionType': 'General'
                }
            })
            
            logger.info(f"eBay message sent for item {item_id}")
            
            return {
                'success': True,
                'method': 'ebay',
                'sent_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"eBay messaging failed: {e}")
            return {'success': False, 'error': str(e)}


class NegotiationManager:
    """
    Manages negotiation flow with sellers
    """
    
    def __init__(self, ai_engine, communicator: SellerCommunicator, config: Dict):
        self.ai_engine = ai_engine
        self.communicator = communicator
        self.config = config
        self.max_attempts = config.get('ai_settings', {}).get('negotiation', {}).get('max_attempts', 3)
    
    async def initiate_negotiation(self, 
                                   opportunity: Dict,
                                   target_price: float) -> Dict:
        """
        Start negotiation with seller
        
        Returns negotiation result with status
        """
        
        logger.info(f"Initiating negotiation for {opportunity['product_title']}")
        
        asking_price = opportunity['source_price']
        
        # Calculate optimal first offer
        first_offer = self.ai_engine.calculate_optimal_offer(
            asking_price=asking_price,
            target_sell_price=opportunity['target_price'],
            min_margin=0.20
        )
        
        # Generate personalized message
        message = self.ai_engine.generate_negotiation_message(
            opportunity=opportunity,
            target_price=first_offer
        )
        
        # Send initial offer
        result = await self.communicator.contact_seller(
            opportunity=opportunity,
            message=message,
            method='auto'
        )
        
        if result['success']:
            negotiation_record = {
                'opportunity_id': opportunity.get('id'),
                'offer_amount': first_offer,
                'message_sent': message,
                'status': 'sent',
                'sent_at': result.get('sent_at'),
                'method': result.get('method'),
                'attempt': 1
            }
            
            logger.info(f"Negotiation initiated: ${first_offer:.2f} offer sent")
            
            return {
                'success': True,
                'negotiation': negotiation_record,
                'next_action': 'wait_for_response'
            }
        else:
            logger.error(f"Failed to send negotiation message: {result.get('error')}")
            return {
                'success': False,
                'error': result.get('error')
            }
    
    async def handle_counter_offer(self,
                                   negotiation: Dict,
                                   counter_price: float,
                                   opportunity: Dict) -> Dict:
        """
        Handle seller's counter offer
        """
        
        logger.info(f"Handling counter offer: ${counter_price:.2f}")
        
        # Analyze counter offer
        min_acceptable = opportunity['source_price'] * 0.85  # Accept up to 85% of asking
        max_profitable = opportunity['target_price'] * 0.75  # Ensure 25% margin
        
        if counter_price <= max_profitable:
            # Accept the counter offer
            logger.info(f"Counter offer ${counter_price:.2f} is acceptable")
            
            acceptance_message = self._generate_acceptance_message(opportunity)
            
            result = await self.communicator.contact_seller(
                opportunity=opportunity,
                message=acceptance_message,
                method=negotiation.get('method', 'auto')
            )
            
            return {
                'decision': 'accept',
                'final_price': counter_price,
                'message_sent': result['success']
            }
            
        elif negotiation.get('attempt', 1) < self.max_attempts:
            # Make another counter offer
            our_counter = (counter_price + max_profitable) / 2  # Meet in middle
            
            counter_message = self._generate_counter_message(opportunity, our_counter)
            
            result = await self.communicator.contact_seller(
                opportunity=opportunity,
                message=counter_message,
                method=negotiation.get('method', 'auto')
            )
            
            return {
                'decision': 'counter',
                'counter_offer': our_counter,
                'message_sent': result['success'],
                'attempt': negotiation.get('attempt', 1) + 1
            }
        else:
            # Too many attempts or unprofitable
            logger.info(f"Declining offer ${counter_price:.2f} - not profitable")
            
            return {
                'decision': 'decline',
                'reason': 'Counter offer not profitable or max attempts reached'
            }
    
    def _generate_acceptance_message(self, opportunity: Dict) -> str:
        """Generate message accepting an offer"""
        
        messages = [
            f"Great! I'll take it at that price. When can I pick it up?",
            f"Perfect, that works for me. What's the best time to meet?",
            f"Sounds good! I'm ready to buy. Can we arrange pickup soon?"
        ]
        
        import random
        return random.choice(messages)
    
    def _generate_counter_message(self, opportunity: Dict, price: float) -> str:
        """Generate counter offer message"""
        
        return f"I appreciate the response. Would you consider ${price:.2f}? I can come pick it up right away with cash in hand."

