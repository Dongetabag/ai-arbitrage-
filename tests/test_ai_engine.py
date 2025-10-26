"""
Tests for AI Engine
"""

import pytest
from core.ai_engine import AIReasoningEngine, ArbitrageOpportunity, DecisionType


@pytest.fixture
def config():
    return {
        'ai_settings': {
            'reasoning': {
                'model': 'gpt-4-turbo-preview',
                'temperature': 0.7
            }
        },
        'categories': {
            'books': {
                'min_margin': 0.25,
                'max_purchase_price': 100
            }
        },
        'automation': {
            'auto_purchase': False
        },
        'risk_management': {
            'max_daily_spend': 2000
        }
    }


@pytest.fixture
def sample_opportunity():
    return ArbitrageOpportunity(
        source_marketplace='craigslist',
        source_price=25.00,
        target_marketplace='amazon',
        target_price=50.00,
        product_title='Calculus Textbook 10th Edition',
        product_category='books',
        product_condition='Good',
        seller_info={'rating': 4.5, 'review_count': 23, 'location': 'Boston, MA'},
        profit_margin=0.35,
        roi=0.80,
        estimated_fees=7.50,
        risk_score=2.0,
        metadata={}
    )


def test_assess_risk(config, sample_opportunity):
    """Test risk assessment"""
    
    engine = AIReasoningEngine(config)
    
    risk_score = engine.assess_risk(sample_opportunity)
    
    assert isinstance(risk_score, float)
    assert 0 <= risk_score <= 10


def test_calculate_optimal_offer(config):
    """Test optimal offer calculation"""
    
    engine = AIReasoningEngine(config)
    
    offer = engine.calculate_optimal_offer(
        asking_price=100.00,
        target_sell_price=200.00,
        min_margin=0.20
    )
    
    assert offer < 100.00  # Should be less than asking
    assert offer > 0


def test_should_purchase_low_margin(config, sample_opportunity):
    """Test purchase decision with low margin"""
    
    engine = AIReasoningEngine(config)
    
    # Set margin too low
    sample_opportunity.profit_margin = 0.10  # Below 0.25 minimum
    
    result = engine.should_purchase(sample_opportunity)
    
    assert result == False


def test_should_purchase_high_price(config, sample_opportunity):
    """Test purchase decision with price too high"""
    
    engine = AIReasoningEngine(config)
    
    # Set price too high
    sample_opportunity.source_price = 150.00  # Above $100 max
    
    result = engine.should_purchase(sample_opportunity)
    
    assert result == False

