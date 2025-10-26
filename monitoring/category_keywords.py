"""
Category-Specific Keywords and Search Terms
Optimized based on the arbitrage report's recommendations
"""

from typing import Dict, List


class CategoryKeywords:
    """Keywords and search strategies for each category"""
    
    # Books & Textbooks
    BOOKS = {
        'primary': [
            'textbook', 'college textbook', 'used textbook',
            'isbn', 'hardcover', 'first edition', 'signed book'
        ],
        'brands': [
            'pearson', 'mcgraw hill', 'cengage', 'wiley',
            'penguin', 'oxford', 'cambridge'
        ],
        'seasonal': {
            'august': ['fall textbook', 'semester book'],
            'january': ['spring textbook', 'winter semester'],
            'may': ['summer textbook']
        },
        'exclude': ['damaged', 'water damage', 'missing pages', 'torn']
    }
    
    # Trading Cards
    TRADING_CARDS = {
        'primary': [
            'pokemon cards', 'pokemon tcg', 'sealed pokemon',
            'magic the gathering', 'mtg', 'magic cards',
            'yugioh', 'yu-gi-oh cards',
            'sports cards', 'baseball cards', 'basketball cards',
            'sealed booster', 'booster box', 'elite trainer box'
        ],
        'high_value': [
            'charizard', 'first edition', 'shadowless',
            'black lotus', 'mox', 'power nine',
            'psa', 'graded', 'gem mint'
        ],
        'exclude': ['fake', 'proxy', 'replica', 'custom']
    }
    
    # Video Games
    VIDEO_GAMES = {
        'primary': [
            'nintendo switch games', 'switch game',
            'ps5 games', 'playstation 5',
            'xbox series x', 'xbox games',
            'retro games', 'vintage games',
            'gameboy', 'game boy', 'nintendo 64',
            'sealed video game', 'new in box', 'cib'
        ],
        'high_value': [
            'limited edition', 'collectors edition',
            'steelbook', 'sealed', 'rare game'
        ],
        'exclude': ['scratched', 'disk only', 'digital code used']
    }
    
    # Musical Instruments
    MUSICAL_INSTRUMENTS = {
        'primary': [
            'guitar', 'electric guitar', 'acoustic guitar',
            'bass guitar', 'keyboard', 'synthesizer',
            'drum set', 'drums', 'amplifier', 'amp',
            'midi controller', 'audio interface', 'microphone'
        ],
        'brands': [
            'fender', 'gibson', 'yamaha', 'roland',
            'korg', 'moog', 'martin', 'taylor',
            'ibanez', 'prs', 'marshall', 'mesa boogie'
        ],
        'exclude': ['broken', 'needs repair', 'for parts']
    }
    
    # LEGO
    LEGO = {
        'primary': [
            'lego set', 'lego', 'legos',
            'lego star wars', 'lego technic', 'lego creator',
            'lego architecture', 'lego city', 'lego ninjago',
            'sealed lego', 'new in box lego', 'retired lego'
        ],
        'high_value': [
            'ucs', 'ultimate collectors series',
            'modular building', 'retired set',
            'millennium falcon', 'death star'
        ],
        'exclude': ['incomplete', 'missing pieces', 'no box', 'mixed pieces']
    }
    
    # Sporting Goods
    SPORTING_GOODS = {
        'primary': [
            'golf clubs', 'golf set', 'driver', 'putter',
            'bike', 'bicycle', 'road bike', 'mountain bike',
            'kayak', 'canoe', 'paddleboard',
            'ski equipment', 'snowboard', 'skis',
            'exercise equipment', 'treadmill', 'weights',
            'fishing gear', 'fishing rod', 'reel'
        ],
        'brands': [
            'trek', 'specialized', 'giant', 'cannondale',
            'callaway', 'titleist', 'ping', 'taylormade',
            'perception', 'hobie', 'old town'
        ],
        'exclude': ['cracked', 'bent', 'rusted']
    }
    
    # Baby Equipment
    BABY_EQUIPMENT = {
        'primary': [
            'stroller', 'baby stroller', 'double stroller',
            'car seat', 'infant car seat', 'convertible car seat',
            'crib', 'baby crib', 'bassinet',
            'high chair', 'baby monitor', 'video monitor',
            'breast pump', 'spectra', 'medela',
            'baby carrier', 'ergo baby', 'baby bjorn'
        ],
        'brands': [
            'uppababy', 'bugaboo', 'britax', 'graco',
            'chicco', 'maclaren', 'babyzen', 'nuna',
            'medela', 'spectra', 'hatch'
        ],
        'exclude': ['recalled', 'expired', 'stained']
    }
    
    # Electronics
    ELECTRONICS = {
        'primary': [
            'laptop', 'macbook', 'macbook pro', 'macbook air',
            'ipad', 'ipad pro', 'ipad air', 'tablet',
            'airpods', 'airpods pro', 'apple watch',
            'gaming console', 'ps5', 'xbox series x', 'nintendo switch',
            'monitor', '4k monitor', 'gaming monitor',
            'graphics card', 'rtx', 'gpu'
        ],
        'high_value': [
            'sealed', 'new in box', 'unopened',
            'apple', 'samsung', 'sony', 'microsoft'
        ],
        'exclude': ['icloud locked', 'activation lock', 'blacklisted', 'for parts']
    }
    
    # Photography Equipment
    PHOTOGRAPHY = {
        'primary': [
            'canon camera', 'nikon camera', 'sony camera',
            'dslr', 'mirrorless', 'full frame',
            'lens', 'canon lens', 'nikon lens', 'sony lens',
            'tripod', 'manfrotto', 'gitzo',
            'flash', 'speedlight', 'strobe',
            'camera bag', 'lowepro', 'peak design',
            'drone', 'dji', 'mavic'
        ],
        'brands': [
            'canon', 'nikon', 'sony', 'fujifilm', 'olympus',
            'panasonic', 'leica', 'hasselblad', 'pentax'
        ],
        'exclude': ['fungus', 'haze', 'broken', 'jammed']
    }
    
    # Tools
    TOOLS = {
        'primary': [
            'dewalt', 'milwaukee', 'makita', 'ryobi',
            'power drill', 'impact driver', 'saw',
            'circular saw', 'miter saw', 'table saw',
            'tool set', 'tool kit', 'mechanics tools',
            'air compressor', 'nail gun', 'sander'
        ],
        'high_value': [
            'cordless', 'brushless', '20v', '18v',
            'combo kit', 'tool set', 'new in box'
        ],
        'exclude': ['no battery', 'no charger', 'broken']
    }
    
    @classmethod
    def get_keywords(cls, category: str) -> List[str]:
        """Get all keywords for a category"""
        
        category_data = getattr(cls, category.upper(), {})
        
        if not category_data:
            return [category]
        
        keywords = category_data.get('primary', [])
        keywords.extend(category_data.get('brands', []))
        
        # Add seasonal keywords if applicable
        seasonal = category_data.get('seasonal', {})
        if seasonal:
            # Add current month's keywords
            from datetime import datetime
            current_month = datetime.now().strftime('%B').lower()
            if current_month in seasonal:
                keywords.extend(seasonal[current_month])
        
        return keywords
    
    @classmethod
    def get_exclude_terms(cls, category: str) -> List[str]:
        """Get exclusion terms for a category"""
        
        category_data = getattr(cls, category.upper(), {})
        return category_data.get('exclude', [])
    
    @classmethod
    def should_exclude(cls, title: str, category: str) -> bool:
        """Check if listing should be excluded based on keywords"""
        
        exclude_terms = cls.get_exclude_terms(category)
        title_lower = title.lower()
        
        return any(term in title_lower for term in exclude_terms)

