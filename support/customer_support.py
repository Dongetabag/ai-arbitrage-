"""
Customer Support Module
AI-powered customer support system
"""

from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger
from enum import Enum


class TicketCategory(Enum):
    SHIPPING = "shipping"
    RETURNS = "returns"
    PRODUCT_QUESTION = "product_question"
    PAYMENT = "payment"
    DAMAGED = "damaged"
    NOT_AS_DESCRIBED = "not_as_described"
    OTHER = "other"


class CustomerSupportAI:
    """
    AI-powered customer support system
    """
    
    def __init__(self, ai_engine, config: Dict):
        self.ai_engine = ai_engine
        self.config = config
        self.auto_respond = config.get('automation', {}).get('auto_respond_support', True)
        self.escalation_keywords = [
            'refund', 'lawyer', 'attorney', 'sue', 'scam', 
            'fraud', 'police', 'federal', 'bbb', 'attorney general'
        ]
    
    async def handle_inquiry(self,
                            customer_message: str,
                            order_context: Dict) -> Dict:
        """
        Handle customer inquiry
        
        Args:
            customer_message: Customer's message
            order_context: Order details and context
            
        Returns:
            Response dict with message and actions
        """
        
        logger.info(f"Handling customer inquiry for order {order_context.get('order_id')}")
        
        # Categorize inquiry
        category = self._categorize_inquiry(customer_message)
        
        # Check if requires escalation
        if self._requires_escalation(customer_message, category):
            return {
                'auto_respond': False,
                'escalate': True,
                'category': category.value,
                'priority': 'high',
                'reason': 'Escalation keywords detected'
            }
        
        # Generate AI response
        response_text = self.ai_engine.generate_customer_support_response(
            customer_message=customer_message,
            order_context=order_context
        )
        
        # Determine if we should auto-send or require review
        confidence = self._assess_response_confidence(customer_message, category)
        
        result = {
            'category': category.value,
            'response': response_text,
            'confidence': confidence,
            'auto_respond': self.auto_respond and confidence > 0.8,
            'escalate': False,
            'suggested_actions': self._suggest_actions(category, order_context)
        }
        
        return result
    
    def _categorize_inquiry(self, message: str) -> TicketCategory:
        """Categorize customer inquiry"""
        
        message_lower = message.lower()
        
        shipping_keywords = ['tracking', 'shipped', 'delivery', 'when will', 'arrive']
        if any(kw in message_lower for kw in shipping_keywords):
            return TicketCategory.SHIPPING
        
        return_keywords = ['return', 'refund', 'send back', 'not want']
        if any(kw in message_lower for kw in return_keywords):
            return TicketCategory.RETURNS
        
        damaged_keywords = ['broken', 'damaged', 'defective', 'not working']
        if any(kw in message_lower for kw in damaged_keywords):
            return TicketCategory.DAMAGED
        
        question_keywords = ['how to', 'does it', 'can i', 'question']
        if any(kw in message_lower for kw in question_keywords):
            return TicketCategory.PRODUCT_QUESTION
        
        return TicketCategory.OTHER
    
    def _requires_escalation(self, message: str, category: TicketCategory) -> bool:
        """Check if inquiry requires human escalation"""
        
        message_lower = message.lower()
        
        # Check for escalation keywords
        if any(kw in message_lower for kw in self.escalation_keywords):
            return True
        
        # High-risk categories
        if category in [TicketCategory.DAMAGED, TicketCategory.NOT_AS_DESCRIBED]:
            return True
        
        return False
    
    def _assess_response_confidence(self, message: str, category: TicketCategory) -> float:
        """Assess confidence in AI response"""
        
        # Simple heuristic - could be enhanced
        if category == TicketCategory.PRODUCT_QUESTION:
            return 0.9  # High confidence for product questions
        elif category == TicketCategory.SHIPPING:
            return 0.95  # Very high for tracking inquiries
        elif category == TicketCategory.RETURNS:
            return 0.7  # Medium for returns
        else:
            return 0.6
    
    def _suggest_actions(self, category: TicketCategory, order_context: Dict) -> List[str]:
        """Suggest actions based on inquiry type"""
        
        actions = []
        
        if category == TicketCategory.SHIPPING:
            if not order_context.get('tracking'):
                actions.append('generate_tracking_number')
            actions.append('send_tracking_update')
            
        elif category == TicketCategory.RETURNS:
            actions.append('send_return_label')
            actions.append('initiate_refund_process')
            
        elif category == TicketCategory.DAMAGED:
            actions.append('request_photos')
            actions.append('prepare_replacement_or_refund')
            actions.append('escalate_to_human')
        
        return actions
    
    async def send_response(self,
                           customer_email: str,
                           response_text: str,
                           order_id: str) -> Dict:
        """Send response to customer"""
        
        logger.info(f"Sending support response for order {order_id}")
        
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
            
            message = Mail(
                from_email=os.getenv('NOTIFICATION_EMAIL', 'support@arbitrage.com'),
                to_emails=customer_email,
                subject=f"Re: Order #{order_id}",
                plain_text_content=response_text
            )
            
            response = sg.send(message)
            
            return {
                'success': True,
                'sent_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send support email: {e}")
            return {'success': False, 'error': str(e)}
    
    def handle_return_request(self, order: Dict, reason: str) -> Dict:
        """Process return request"""
        
        logger.info(f"Processing return for order {order.get('id')}")
        
        # Generate return label
        # Process refund
        # Update inventory
        
        return {
            'return_approved': True,
            'return_label_url': 'https://example.com/return-label',
            'refund_amount': order.get('sale_price', 0),
            'refund_status': 'pending'
        }

