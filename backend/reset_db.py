#!/usr/bin/env python3
"""
Reset database by dropping and recreating all tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.session import get_engine, init_engine, Base
from core.config import settings
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """Drop and recreate all tables"""
    try:
        # Initialize database connection
        init_engine(settings.DB_URL)
        engine = get_engine()
        
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                # Drop all tables
                logger.info("Dropping all tables...")
                conn.execute(text("DROP TABLE IF EXISTS extracted_fields CASCADE;"))
                conn.execute(text("DROP TABLE IF EXISTS certificates CASCADE;"))
                conn.execute(text("DROP TABLE IF EXISTS students CASCADE;"))
                conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
                
                # Commit the drops
                trans.commit()
                logger.info("All tables dropped successfully")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"Error dropping tables: {str(e)}")
                raise
        
        # Now recreate all tables using SQLAlchemy
        logger.info("Creating all tables...")
        from db import models  # Import all models
        Base.metadata.create_all(bind=engine)
        logger.info("All tables created successfully!")
        
    except Exception as e:
        logger.error(f"Database reset error: {str(e)}")
        raise

if __name__ == "__main__":
    reset_database()
