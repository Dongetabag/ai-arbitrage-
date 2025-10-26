"""
Core AI Reasoning Engine
Handles decision-making, negotiation strategy, and autonomous actions
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import anthropic
import openai
from loguru import logger


class DecisionType(Enum):
    PURCHASE = "purchase"
    NEGOTIATE = "negotiate"
    LIST = "list"
    RESPOND_CUSTOMER = "respond_customer"
    AUTHENTICATE = "authenticate"
    SKIP = "skip"


@dataclass
class ArbitrageOpportunity:
    """Represents a potential arbitrage deal"""
    source_marketplace: str
    source_price: float
    target_marketplace: str
    target_price: float
    product_title: str
    product_category: str
    product_condition: str
    seller_info: Dict
    profit_margin: float
    roi: float
    estimated_fees: float
    risk_score: float
    metadata: Dict


@dataclass
class AIDecision:
    """AI's decision on an opportunity"""
    decision: DecisionType
    confidence: float
    reasoning: str
    action_params: Dict
    estimated_profit: float
    risks: List[str]


class AIReasoningEngine:
    """
    Main AI engine that reasons about arbitrage opportunities,
    negotiates with sellers, and makes autonomous decisions
    """
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        self.ai_provider = os.getenv('AI_PROVIDER', 'google')  # Default to Google now
        self.ai_model = os.getenv('AI_MODEL', 'gemini-2.5-flash')
        
        # Initialize AI clients based on provider
        if self.ai_provider == 'google' or 'gemini' in self.ai_model.lower():
            # Use Google Gemini
            from core.google_ai_engine import GeminiAIEngine
            self.client = GeminiAIEngine()
            self.use_google = True
            self.use_anthropic = False
            self.use_openai = False
            logger.info(f"✅ AI Engine initialized with Google Gemini 2.5 Flash")
        elif self.ai_provider == 'anthropic' or 'claude' in self.ai_model.lower():
            self.client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            self.use_anthropic = True
            self.use_google = False
            self.use_openai = False
            logger.info(f"✅ AI Engine initialized with Anthropic Claude")
        else:
            # OpenAI (only if explicitly set)
            openai_key = os.getenv('OPENAI_API_KEY')
            if not openai_key:
                logger.warning("No OPENAI_API_KEY found, falling back to Google Gemini")
                from core.google_ai_engine import GeminiAIEngine
                self.client = GeminiAIEngine()
                self.use_google = True
                self.use_anthropic = False
                self.use_openai = False
            else:
                self.client = openai.OpenAI(api_key=openai_key)
                self.use_anthropic = False
                self.use_google = False
                self.use_openai = True
                logger.info(f"✅ AI Engine initialized with OpenAI GPT-4")
    
    def analyze_opportunity(self, opportunity: ArbitrageOpportunity) -> AIDecision:
        """
        Analyze an arbitrage opportunity and decide on action
        """
        logger.info(f"Analyzing opportunity: {opportunity.product_title}")
        
        # Build context for AI
        context = self._build_opportunity_context(opportunity)
        
        # Get AI reasoning
        reasoning_response = self._get_ai_reasoning(context)
        
        # Parse decision
        decision = self._parse_ai_decision(reasoning_response, opportunity)
        
        logger.info(f"Decision: {decision.decision.value} (confidence: {decision.confidence:.2f})")
        
        return decision
    
    def _build_opportunity_context(self, opp: ArbitrageOpportunity) -> str:
        """Build detailed context for AI reasoning"""
        
        category_config = self.config.get('categories', {}).get(opp.product_category, {})
        min_margin = category_config.get('min_margin', 0.20)
        
        context = f"""
ARBITRAGE OPPORTUNITY ANALYSIS

Product Details:
- Title: {opp.product_title}
- Category: {opp.product_category}
- Condition: {opp.product_condition}

Financial Analysis:
- Purchase Price: ${opp.source_price:.2f}
- Estimated Sell Price: ${opp.target_price:.2f}
- Gross Profit: ${opp.target_price - opp.source_price:.2f}
- Estimated Fees: ${opp.estimated_fees:.2f}
- Net Profit: ${opp.target_price - opp.source_price - opp.estimated_fees:.2f}
- Profit Margin: {opp.profit_margin*100:.1f}%
- ROI: {opp.roi*100:.1f}%
- Minimum Required Margin: {min_margin*100:.1f}%

Marketplaces:
- Source: {opp.source_marketplace}
- Target: {opp.target_marketplace}

Seller Information:
- Rating: {opp.seller_info.get('rating', 'N/A')}
- Reviews: {opp.seller_info.get('review_count', 'N/A')}
- Location: {opp.seller_info.get('location', 'N/A')}
- Response Rate: {opp.seller_info.get('response_rate', 'N/A')}

Risk Assessment:
- Risk Score: {opp.risk_score:.2f}/10
- Authentication Required: {'Yes' if opp.target_price > 300 else 'No'}

Category Metadata:
{opp.metadata}

Your task: Analyze this opportunity and decide:
1. Should we PURCHASE (meets all criteria)
2. Should we NEGOTIATE (try to get better price)
3. Should we SKIP (not profitable/too risky)
4. Should we AUTHENTICATE (need verification first)

Provide your decision with clear reasoning, confidence score (0-1), and specific action parameters.
"""
        return context
    
    def _get_ai_reasoning(self, context: str) -> str:
        """Get reasoning from AI model"""
        
        system_prompt = """You are an expert arbitrage analyst with deep knowledge of online reselling, 
pricing strategies, and risk management. You analyze opportunities with a critical eye, considering:
- Profit margins and ROI
- Market demand and competition
- Seller reliability and risk factors
- Product authenticity concerns
- Fees and hidden costs
- Time to sell and capital efficiency

Be conservative with high-risk items and aggressive with proven profitable categories.
Always output decisions in this format:

DECISION: [PURCHASE|NEGOTIATE|SKIP|AUTHENTICATE]
CONFIDENCE: [0.0-1.0]
REASONING: [Your detailed reasoning]
ACTION_PARAMS: [JSON object with specific parameters]
ESTIMATED_PROFIT: [dollar amount]
RISKS: [comma-separated list of risks]
"""
        
        try:
            if self.use_google:
                # Use Google Gemini
                return self.client.analyze_opportunity(context)
            elif self.use_anthropic:
                response = self.client.messages.create(
                    model=self.ai_model,
                    max_tokens=2000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": context}]
                )
                return response.content[0].text
            else:
                # OpenAI
                response = self.client.chat.completions.create(
                    model=self.ai_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": context}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"AI reasoning failed: {e}")
            # Fallback to rule-based decision
            return self._fallback_reasoning(context)
    
    def _parse_ai_decision(self, response: str, opp: ArbitrageOpportunity) -> AIDecision:
        """Parse AI response into structured decision"""
        
        lines = response.strip().split('\n')
        decision_map = {
            'PURCHASE': DecisionType.PURCHASE,
            'NEGOTIATE': DecisionType.NEGOTIATE,
            'SKIP': DecisionType.SKIP,
            'AUTHENTICATE': DecisionType.AUTHENTICATE
        }
        
        decision = DecisionType.SKIP
        confidence = 0.5
        reasoning = "AI analysis"
        action_params = {}
        estimated_profit = 0.0
        risks = []
        
        for line in lines:
            if line.startswith('DECISION:'):
                decision_str = line.split(':', 1)[1].strip()
                decision = decision_map.get(decision_str, DecisionType.SKIP)
                
            elif line.startswith('CONFIDENCE:'):
                try:
                    confidence = float(line.split(':', 1)[1].strip())
                except:
                    confidence = 0.5
                    
            elif line.startswith('REASONING:'):
                reasoning = line.split(':', 1)[1].strip()
                
            elif line.startswith('ACTION_PARAMS:'):
                import json
                try:
                    action_params = json.loads(line.split(':', 1)[1].strip())
                except:
                    action_params = {}
                    
            elif line.startswith('ESTIMATED_PROFIT:'):
                try:
                    profit_str = line.split(':', 1)[1].strip().replace('$', '').replace(',', '')
                    estimated_profit = float(profit_str)
                except:
                    estimated_profit = opp.target_price - opp.source_price - opp.estimated_fees
                    
            elif line.startswith('RISKS:'):
                risks = [r.strip() for r in line.split(':', 1)[1].split(',')]
        
        return AIDecision(
            decision=decision,
            confidence=confidence,
            reasoning=reasoning,
            action_params=action_params,
            estimated_profit=estimated_profit,
            risks=risks
        )
    
    def _fallback_reasoning(self, context: str) -> str:
        """Simple rule-based fallback if AI fails"""
        return """
DECISION: SKIP
CONFIDENCE: 0.3
REASONING: AI service unavailable, defaulting to conservative approach
ACTION_PARAMS: {}
ESTIMATED_PROFIT: 0
RISKS: AI service error, unable to analyze properly
"""
    
    def generate_negotiation_message(self, 
                                    opportunity: ArbitrageOpportunity,
                                    target_price: float) -> str:
        """Generate personalized negotiation message"""
        
        prompt = f"""
Generate a friendly, persuasive negotiation message for this scenario:

Product: {opportunity.product_title}
Current Asking Price: ${opportunity.source_price:.2f}
Our Target Price: ${target_price:.2f}
Marketplace: {opportunity.source_marketplace}
Seller Rating: {opportunity.seller_info.get('rating', 'N/A')}

The message should:
- Be friendly and respectful
- Show genuine interest in the item
- Provide a reasonable justification for the lower offer
- Leave room for counter-offers
- Be concise (2-3 sentences)

Generate only the message text, no additional commentary.
"""
        
        try:
            if self.use_anthropic:
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
                
        except Exception as e:
            logger.error(f"Failed to generate negotiation message: {e}")
            return f"Hi! I'm interested in your {opportunity.product_title}. Would you consider ${target_price:.2f}? I can pick up today. Thanks!"
    
    def generate_customer_support_response(self, 
                                          customer_message: str,
                                          order_context: Dict) -> str:
        """Generate customer support response"""
        
        prompt = f"""
You are a professional customer support agent for an online marketplace seller.

Customer Message: {customer_message}

Order Context:
- Product: {order_context.get('product_name', 'N/A')}
- Order Date: {order_context.get('order_date', 'N/A')}
- Order Status: {order_context.get('status', 'N/A')}
- Tracking: {order_context.get('tracking', 'N/A')}

Generate a helpful, professional, and empathetic response that:
- Addresses their concern directly
- Provides relevant information
- Offers a solution if applicable
- Maintains a positive tone
- Is concise but complete

Generate only the response text.
"""
        
        try:
            if self.use_anthropic:
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text.strip()
            else:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=500
                )
                return response.choices[0].message.content.strip()
                
        except Exception as e:
            logger.error(f"Failed to generate support response: {e}")
            return "Thank you for contacting us. We're looking into your inquiry and will respond shortly with more information."
    
    def generate_product_listing(self, product_data: Dict) -> Dict[str, str]:
        """Generate optimized product listing title and description"""
        
        prompt = f"""
Create an optimized product listing for:

Product: {product_data.get('title')}
Category: {product_data.get('category')}
Condition: {product_data.get('condition')}
Key Features: {product_data.get('features', [])}
Brand: {product_data.get('brand', 'N/A')}

Generate:
1. TITLE: SEO-optimized title (80 chars max, include key searchable terms)
2. DESCRIPTION: Compelling description highlighting value, condition, and features (200-300 words)
3. BULLET_POINTS: 5 key selling points

Format as:
TITLE: [title]
DESCRIPTION: [description]
BULLET_POINTS:
- [point 1]
- [point 2]
...
"""
        
        try:
            if self.use_anthropic:
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.content[0].text
            else:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=1000
                )
                content = response.choices[0].message.content
            
            # Parse response
            listing = self._parse_listing_response(content)
            return listing
            
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
            'title': title[:80],  # Enforce length limit
            'description': description.strip(),
            'bullet_points': bullet_points[:5]  # Max 5 points
        }
    
    def should_purchase(self, opportunity: ArbitrageOpportunity) -> bool:
        """
        Final decision gate before purchase
        Combines AI reasoning with hard rules
        """
        # Hard rule checks
        category_config = self.config.get('categories', {}).get(opportunity.product_category, {})
        min_margin = category_config.get('min_margin', 0.20)
        max_price = category_config.get('max_purchase_price', 500)
        
        # Check hard limits
        if opportunity.source_price > max_price:
            logger.warning(f"Price ${opportunity.source_price} exceeds max ${max_price}")
            return False
            
        if opportunity.profit_margin < min_margin:
            logger.warning(f"Margin {opportunity.profit_margin:.2%} below min {min_margin:.2%}")
            return False
        
        # Check daily spend limit
        max_daily = self.config.get('risk_management', {}).get('max_daily_spend', 2000)
        # TODO: Query database for today's spend
        
        # Get AI decision
        decision = self.analyze_opportunity(opportunity)
        
        if decision.decision != DecisionType.PURCHASE:
            return False
            
        if decision.confidence < 0.7:
            logger.warning(f"AI confidence {decision.confidence:.2f} below threshold 0.7")
            return False
        
        # Check if manual approval required
        auto_purchase = self.config.get('automation', {}).get('auto_purchase', False)
        if not auto_purchase and opportunity.source_price > 100:
            logger.info("Manual approval required for purchases over $100")
            return False
        
        return True
    
    def calculate_optimal_offer(self, 
                               asking_price: float,
                               target_sell_price: float,
                               min_margin: float) -> float:
        """Calculate optimal negotiation offer price"""
        
        # Target margin + 10% buffer for fees and negotiation room
        target_margin = min_margin + 0.10
        
        # Calculate max we can pay to achieve target margin
        max_purchase_price = target_sell_price * (1 - target_margin)
        
        # Start 15-20% below asking price for negotiation room
        optimal_offer = asking_price * 0.80
        
        # Don't offer more than our max
        optimal_offer = min(optimal_offer, max_purchase_price)
        
        # Round to nearest $5 for psychological pricing
        optimal_offer = round(optimal_offer / 5) * 5
        
        logger.info(f"Optimal offer: ${optimal_offer:.2f} (asking: ${asking_price:.2f}, max: ${max_purchase_price:.2f})")
        
        return optimal_offer
    
    def assess_risk(self, opportunity: ArbitrageOpportunity) -> float:
        """
        Calculate risk score (0-10, higher = riskier)
        """
        risk_score = 0.0
        
        # Price risk
        if opportunity.source_price > 500:
            risk_score += 2.0
        elif opportunity.source_price > 300:
            risk_score += 1.0
            
        # Seller risk
        seller_rating = opportunity.seller_info.get('rating', 0)
        if seller_rating < 4.0:
            risk_score += 2.0
        elif seller_rating < 4.5:
            risk_score += 1.0
            
        review_count = opportunity.seller_info.get('review_count', 0)
        if review_count < 5:
            risk_score += 1.5
        elif review_count < 20:
            risk_score += 0.5
            
        # Condition risk
        if opportunity.product_condition.lower() in ['poor', 'fair', 'for parts']:
            risk_score += 2.0
        elif opportunity.product_condition.lower() == 'good':
            risk_score += 0.5
            
        # Category risk
        high_fraud_categories = ['electronics', 'photography', 'trading_cards']
        if opportunity.product_category in high_fraud_categories:
            risk_score += 1.0
            
        # Margin risk (too good to be true?)
        if opportunity.profit_margin > 0.50:
            risk_score += 1.5  # Suspiciously high margin
            
        return min(risk_score, 10.0)

