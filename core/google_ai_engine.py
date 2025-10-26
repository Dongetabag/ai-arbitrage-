"""
Google Gemini AI Integration
Adapter for using Gemini Pro as the AI reasoning engine
"""

import os
import google.generativeai as genai
from typing import Dict, Optional
from loguru import logger


class GeminiAIEngine:
    """
    Google Gemini AI integration for arbitrage reasoning
    """
    
    def __init__(self):
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Initialize model (use latest Gemini 2.5 Flash - fast and powerful!)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        logger.info("✅ Google Gemini AI initialized")
    
    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate AI response using Gemini
        
        Args:
            prompt: User prompt
            system_prompt: System instructions (prepended to prompt)
            
        Returns:
            AI response text
        """
        
        try:
            # Combine system prompt with user prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def analyze_opportunity(self, context: str) -> str:
        """Analyze arbitrage opportunity"""
        
        system_prompt = """You are an expert arbitrage analyst. Analyze opportunities critically considering:
- Profit margins and ROI
- Market demand and competition
- Seller reliability
- Product authenticity
- Fees and hidden costs

Output format:
DECISION: [PURCHASE|NEGOTIATE|SKIP|AUTHENTICATE]
CONFIDENCE: [0.0-1.0]
REASONING: [Your reasoning]
ACTION_PARAMS: {}
ESTIMATED_PROFIT: [dollar amount]
RISKS: [risks]
"""
        
        return self.generate_response(context, system_prompt)
    
    def generate_negotiation_message(self, opportunity: Dict, target_price: float) -> str:
        """Generate negotiation message"""
        
        prompt = f"""Generate a friendly negotiation message:

Product: {opportunity.get('product_title', 'item')}
Asking Price: ${opportunity.get('source_price', 0):.2f}
Your Offer: ${target_price:.2f}

Make it friendly, brief (2-3 sentences), and persuasive.
Only output the message text.
"""
        
        try:
            return self.generate_response(prompt)
        except:
            return f"Hi! I'm interested in your {opportunity.get('product_title', 'item')}. Would you consider ${target_price:.2f}? Thanks!"
    
    def generate_customer_support_response(self, message: str, context: Dict) -> str:
        """Generate customer support response"""
        
        prompt = f"""You are a professional customer support agent.

Customer message: {message}
Order context: {context}

Generate a helpful, professional response.
Only output the response text.
"""
        
        try:
            return self.generate_response(prompt)
        except:
            return "Thank you for contacting us. We're looking into your inquiry and will respond shortly."
    
    def generate_product_listing(self, product_data: Dict) -> Dict[str, str]:
        """Generate optimized product listing"""
        
        prompt = f"""Create an optimized product listing:

Product: {product_data.get('title')}
Category: {product_data.get('category')}
Condition: {product_data.get('condition')}

Generate:
TITLE: [SEO-optimized, 80 chars max]
DESCRIPTION: [Compelling, 200-300 words]
BULLET_POINTS:
- [point 1]
- [point 2]
- [point 3]
- [point 4]
- [point 5]
"""
        
        try:
            response = self.generate_response(prompt)
            return self._parse_listing_response(response)
        except Exception as e:
            logger.error(f"Failed to generate listing: {e}")
            return {
                'title': product_data.get('title', ''),
                'description': product_data.get('title', ''),
                'bullet_points': []
            }
    
    def _parse_listing_response(self, response: str) -> Dict[str, str]:
        """Parse listing generation response"""
        
        lines = response.strip().split('\n')
        
        title = ""
        description = ""
        bullet_points = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('TITLE:'):
                title = line.split(':', 1)[1].strip()
                current_section = 'title'
            elif line.startswith('DESCRIPTION:'):
                description = line.split(':', 1)[1].strip()
                current_section = 'description'
            elif line.startswith('BULLET_POINTS:'):
                current_section = 'bullets'
            elif line.startswith('-') and current_section == 'bullets':
                bullet_points.append(line[1:].strip())
            elif current_section == 'description' and line and not line.startswith('BULLET'):
                description += ' ' + line
        
        return {
            'title': title[:80],
            'description': description.strip(),
            'bullet_points': bullet_points[:5]
        }

