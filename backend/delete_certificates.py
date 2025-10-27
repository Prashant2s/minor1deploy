#!/usr/bin/env python3
"""
Delete all certificate records from the database.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import get_engine, init_engine
from app.core.config import settings
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_all_certificates():
    """Delete all certificate records and related data"""
    try:
        # Initialize database connection
        init_engine(settings.DB_URL)
        engine = get_engine()
        
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                # Check if tables exist and delete records
                try:
                    # Delete all extracted fields first (foreign key dependency)
                    logger.info("Deleting all extracted fields...")
                    result = conn.execute(text("DELETE FROM extracted_fields;"))
                    logger.info(f"Deleted {result.rowcount} extracted field records")
                except Exception as e:
                    logger.warning(f"Could not delete extracted_fields: {str(e)}")
                
                try:
                    # Delete all certificates
                    logger.info("Deleting all certificates...")
                    result = conn.execute(text("DELETE FROM certificates;"))
                    logger.info(f"Deleted {result.rowcount} certificate records")
                except Exception as e:
                    logger.warning(f"Could not delete certificates: {str(e)}")
                
                # Commit the transaction
                trans.commit()
                logger.info("All certificate records deleted successfully!")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"Error deleting records: {str(e)}")
                raise
        
    except Exception as e:
        logger.error(f"Database operation error: {str(e)}")
        raise

if __name__ == "__main__":
    confirm = input("Are you sure you want to delete ALL certificate records? (yes/no): ")
    if confirm.lower() == 'yes':
        delete_all_certificates()
        print("\n✓ All certificate records have been deleted.")
    else:
        print("Operation cancelled.")
