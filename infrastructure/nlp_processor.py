"""
NLP Processing with spaCy and NLTK
For intelligent product matching, description analysis, and chatbot support
"""

import spacy
from typing import List, Dict, Tuple
from loguru import logger
import re


class NLPProcessor:
    """
    Natural Language Processing for product data extraction
    Uses spaCy for context-aware analysis
    """
    
    def __init__(self):
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded")
        except OSError:
            logger.warning("spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def extract_product_info(self, title: str, description: str = "") -> Dict:
        """
        Extract structured information from product listing
        
        Returns:
            {
                'brand': str,
                'model': str,
                'condition_indicators': List[str],
                'key_features': List[str],
                'entities': List[Tuple[str, str]]
            }
        """
        
        if not self.nlp:
            return self._fallback_extraction(title, description)
        
        # Process text
        doc = self.nlp(title + " " + description)
        
        # Extract named entities
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        
        # Identify brand (ORG entities)
        brands = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
        brand = brands[0] if brands else None
        
        # Extract model numbers
        model_pattern = r'\b[A-Z0-9]{3,}[-]?[A-Z0-9]{2,}\b'
        models = re.findall(model_pattern, title.upper())
        model = models[0] if models else None
        
        # Condition indicators
        condition_keywords = {
            'new': ['new', 'sealed', 'unopened', 'nib', 'brand new'],
            'like_new': ['like new', 'mint', 'pristine', 'barely used'],
            'good': ['good condition', 'gently used', 'light use'],
            'fair': ['fair', 'signs of wear', 'used'],
            'poor': ['poor', 'damaged', 'for parts', 'broken']
        }
        
        text_lower = (title + " " + description).lower()
        condition_indicators = []
        
        for condition, keywords in condition_keywords.items():
            if any(kw in text_lower for kw in keywords):
                condition_indicators.append(condition)
        
        # Extract key features (noun chunks)
        key_features = [chunk.text for chunk in doc.noun_chunks][:5]
        
        return {
            'brand': brand,
            'model': model,
            'condition_indicators': condition_indicators,
            'key_features': key_features,
            'entities': entities,
            'keywords': self._extract_keywords(doc)
        }
    
    def _extract_keywords(self, doc) -> List[str]:
        """Extract important keywords"""
        
        # Filter for nouns, proper nouns, adjectives
        keywords = [
            token.text.lower()
            for token in doc
            if token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and not token.is_stop
        ]
        
        return list(set(keywords))[:10]  # Top 10 unique keywords
    
    def _fallback_extraction(self, title: str, description: str) -> Dict:
        """Fallback extraction without spaCy"""
        
        # Simple regex-based extraction
        model_pattern = r'\b[A-Z0-9]{3,}[-]?[A-Z0-9]{2,}\b'
        models = re.findall(model_pattern, title.upper())
        
        return {
            'brand': None,
            'model': models[0] if models else None,
            'condition_indicators': [],
            'key_features': title.split()[:5],
            'entities': [],
            'keywords': []
        }
    
    def calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two product descriptions
        
        Useful for:
        - Matching listings to Amazon products
        - Detecting duplicates
        - Finding comparable items
        """
        
        if not self.nlp:
            return 0.0
        
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)
        
        # Use spaCy's built-in similarity
        similarity = doc1.similarity(doc2)
        
        return similarity
    
    def extract_isbn(self, text: str) -> Optional[str]:
        """Extract ISBN from text using NLP + regex"""
        
        # ISBN-13
        isbn13_pattern = r'(?:ISBN[-]?13?[:]?\s*)?(?:97[89][-\s]?(?:\d[-\s]?){9}\d)'
        match = re.search(isbn13_pattern, text, re.IGNORECASE)
        if match:
            return re.sub(r'[-\s]', '', match.group())
        
        # ISBN-10
        isbn10_pattern = r'(?:ISBN[-]?10?[:]?\s*)?(?:\d[-\s]?){9}[\dXx]'
        match = re.search(isbn10_pattern, text, re.IGNORECASE)
        if match:
            return re.sub(r'[-\s]', '', match.group())
        
        return None
    
    def sentiment_analysis(self, text: str) -> str:
        """
        Analyze sentiment of customer message
        
        Returns: 'positive', 'neutral', 'negative'
        """
        
        # Simple sentiment based on keywords
        positive_words = ['great', 'excellent', 'perfect', 'love', 'awesome', 'thanks']
        negative_words = ['terrible', 'awful', 'hate', 'scam', 'fraud', 'broken', 'damaged']
        
        text_lower = text.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        else:
            return 'neutral'


class ChatbotNLP:
    """
    NLP for intelligent chatbot/customer support
    Provides context-aware responses
    """
    
    def __init__(self):
        self.nlp_processor = NLPProcessor()
    
    def classify_intent(self, message: str) -> str:
        """
        Classify customer message intent
        
        Intents:
        - shipping_inquiry
        - return_request
        - product_question
        - complaint
        - compliment
        """
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['track', 'shipping', 'delivery', 'arrive']):
            return 'shipping_inquiry'
        
        if any(word in message_lower for word in ['return', 'refund', 'send back']):
            return 'return_request'
        
        if any(word in message_lower for word in ['how', 'does', 'can', 'will', 'question']):
            return 'product_question'
        
        if any(word in message_lower for word in ['terrible', 'awful', 'scam', 'angry']):
            return 'complaint'
        
        if any(word in message_lower for word in ['great', 'excellent', 'perfect', 'thanks']):
            return 'compliment'
        
        return 'general'
    
    def extract_entities_from_message(self, message: str) -> Dict:
        """
        Extract key information from customer message
        
        Example: "Where is my order #12345?"
        Returns: {'order_number': '12345'}
        """
        
        entities = {}
        
        # Extract order number
        order_match = re.search(r'#?(\d{5,})', message)
        if order_match:
            entities['order_number'] = order_match.group(1)
        
        # Extract email
        email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', message)
        if email_match:
            entities['email'] = email_match.group()
        
        # Extract phone number
        phone_match = re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', message)
        if phone_match:
            entities['phone'] = phone_match.group()
        
        return entities

