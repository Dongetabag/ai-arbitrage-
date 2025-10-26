"""
Utility Functions and Helpers
"""

import re
from typing import Optional
from datetime import datetime, timedelta


def extract_isbn(text: str) -> Optional[str]:
    """Extract ISBN from text"""
    
    # ISBN-13 pattern
    isbn13_pattern = r'97[89][-\s]?(?:\d[-\s]?){9}\d'
    match = re.search(isbn13_pattern, text)
    if match:
        return re.sub(r'[-\s]', '', match.group())
    
    # ISBN-10 pattern
    isbn10_pattern = r'(?:\d[-\s]?){9}[\dXx]'
    match = re.search(isbn10_pattern, text)
    if match:
        return re.sub(r'[-\s]', '', match.group())
    
    return None


def extract_upc(text: str) -> Optional[str]:
    """Extract UPC from text"""
    
    upc_pattern = r'\b\d{12}\b'
    match = re.search(upc_pattern, text)
    if match:
        return match.group()
    
    return None


def calculate_fees(price: float, marketplace: str, category: str) -> float:
    """Calculate marketplace fees"""
    
    fees = 0.0
    
    if marketplace == 'amazon':
        # Amazon referral fees
        if category == 'books':
            fees = 1.80 + (price * 0.15)  # $1.80 + 15%
        else:
            fees = price * 0.15  # 15% referral fee
        
        # FBA fulfillment fees (estimated)
        if price < 20:
            fees += 3.00
        elif price < 50:
            fees += 4.50
        else:
            fees += 6.00
            
    elif marketplace == 'ebay':
        # eBay fees: 12.9% final value fee
        fees = price * 0.129
        
        # PayPal fees: 2.9% + $0.30
        fees += (price * 0.029) + 0.30
    
    return round(fees, 2)


def calculate_roi(profit: float, cost: float) -> float:
    """Calculate return on investment"""
    
    if cost == 0:
        return 0.0
    
    return (profit / cost) * 100


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"


def parse_price(price_text: str) -> float:
    """Parse price from text"""
    
    # Remove currency symbols and commas
    cleaned = re.sub(r'[$,]', '', price_text)
    
    # Extract first number
    match = re.search(r'\d+\.?\d*', cleaned)
    if match:
        return float(match.group())
    
    return 0.0


def is_profitable(source_price: float,
                  target_price: float,
                  fees: float,
                  min_margin: float = 0.20) -> bool:
    """Check if opportunity is profitable"""
    
    total_cost = source_price + fees
    profit = target_price - total_cost
    margin = profit / target_price if target_price > 0 else 0
    
    return margin >= min_margin and profit >= 10  # Min $10 profit


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    
    # Remove unsafe characters
    safe = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Limit length
    return safe[:255]


def generate_sku(category: str, timestamp: Optional[datetime] = None) -> str:
    """Generate unique SKU"""
    
    if not timestamp:
        timestamp = datetime.utcnow()
    
    # Format: CATEGORY-YYYYMMDD-HHMMSS
    category_code = category[:3].upper()
    date_str = timestamp.strftime('%Y%m%d-%H%M%S')
    
    return f"{category_code}-{date_str}"


def estimate_shipping_cost(weight_lbs: float, 
                          size: str = 'medium',
                          service: str = 'standard') -> float:
    """Estimate shipping cost"""
    
    # Simplified shipping cost estimation
    base_costs = {
        'small': 5.00,
        'medium': 8.00,
        'large': 15.00,
        'oversized': 25.00
    }
    
    base = base_costs.get(size, 8.00)
    
    # Add weight factor
    if weight_lbs > 5:
        base += (weight_lbs - 5) * 0.50
    
    # Service multiplier
    if service == 'expedited':
        base *= 1.5
    elif service == 'overnight':
        base *= 2.5
    
    return round(base, 2)


def days_until(target_date: datetime) -> int:
    """Calculate days until target date"""
    
    delta = target_date - datetime.utcnow()
    return max(0, delta.days)


def is_valid_email(email: str) -> bool:
    """Validate email address"""
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """Validate US phone number"""
    
    # Remove formatting
    digits = re.sub(r'\D', '', phone)
    
    # Check if 10 or 11 digits (with country code)
    return len(digits) in [10, 11]

