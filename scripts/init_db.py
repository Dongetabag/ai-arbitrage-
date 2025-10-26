"""
Database Initialization Script
Creates all tables and initial data
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.models import Base
from sqlalchemy import create_engine
import os


def init_database():
    """Initialize database"""
    
    db_url = os.getenv('DATABASE_URL', 'sqlite:///arbitrage.db')
    
    print(f"Initializing database: {db_url}")
    
    engine = create_engine(db_url, echo=True)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print("✓ Database initialized successfully")
    print("\nTables created:")
    for table in Base.metadata.tables.keys():
        print(f"  - {table}")


if __name__ == "__main__":
    init_database()

