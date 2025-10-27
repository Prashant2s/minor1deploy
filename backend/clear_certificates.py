#!/usr/bin/env python3
"""
Delete all certificate records from the database using ORM.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import db_session, init_engine
from app.db.models import Certificate, ExtractedField
from app.core.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_all_certificates():
    """Delete all certificate records using ORM"""
    try:
        # Initialize database
        init_engine(settings.DB_URL)
        
        # Count records before deletion
        cert_count = db_session.query(Certificate).count()
        field_count = db_session.query(ExtractedField).count()
        
        logger.info(f"Found {cert_count} certificates and {field_count} extracted fields")
        
        if cert_count == 0:
            logger.info("No certificates to delete.")
            return
        
        # Delete all certificates (cascade will delete extracted fields)
        logger.info("Deleting all certificates...")
        db_session.query(Certificate).delete()
        db_session.commit()
        
        logger.info(f"✓ Successfully deleted {cert_count} certificates and their associated data")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        db_session.rollback()
        raise

if __name__ == "__main__":
    confirm = input("Are you sure you want to delete ALL certificate records? (yes/no): ")
    if confirm.lower() == 'yes':
        delete_all_certificates()
        print("\n✓ All certificate records have been deleted.")
    else:
        print("Operation cancelled.")
