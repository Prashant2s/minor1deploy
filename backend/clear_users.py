#!/usr/bin/env python3
"""
Clear all user login details and related data from the database.
This will remove all users, their certificates, and extracted fields.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import init_engine, db_session
from app.core.config import settings
from app.db.models import User, Certificate, ExtractedField, Student
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_all_users():
    """Remove all user login details and related data"""
    try:
        # Initialize database connection
        init_engine(settings.DB_URL)
        
        with db_session.begin():
            # Count existing data
            user_count = db_session.query(User).count()
            cert_count = db_session.query(Certificate).count()
            field_count = db_session.query(ExtractedField).count()
            student_count = db_session.query(Student).count()
            
            logger.info(f"Found {user_count} users, {cert_count} certificates, {field_count} extracted fields, {student_count} students")
            
            if user_count == 0:
                logger.info("No users found to delete")
                return
            
            # Delete in order to respect foreign key constraints
            logger.info("Deleting extracted fields...")
            deleted_fields = db_session.query(ExtractedField).delete(synchronize_session=False)
            logger.info(f"Deleted {deleted_fields} extracted fields")
            
            logger.info("Deleting certificates...")
            deleted_certs = db_session.query(Certificate).delete(synchronize_session=False)
            logger.info(f"Deleted {deleted_certs} certificates")
            
            logger.info("Deleting students...")
            deleted_students = db_session.query(Student).delete(synchronize_session=False)
            logger.info(f"Deleted {deleted_students} students")
            
            logger.info("Deleting users...")
            deleted_users = db_session.query(User).delete(synchronize_session=False)
            logger.info(f"Deleted {deleted_users} users")
            
            # Commit all changes
            db_session.commit()
            
            logger.info("✅ All user login details and related data have been successfully removed!")
            logger.info(f"Summary: {deleted_users} users, {deleted_certs} certificates, {deleted_fields} fields, {deleted_students} students deleted")
            
    except Exception as e:
        db_session.rollback()
        logger.error(f"Error clearing user data: {str(e)}")
        raise

if __name__ == "__main__":
    print("⚠️  WARNING: This will delete ALL user login details and related data!")
    print("This includes:")
    print("- All user accounts and login credentials")
    print("- All uploaded certificates")
    print("- All extracted field data")
    print("- All student records")
    print()
    
    # Auto-confirm for automated execution
    print("Proceeding with deletion...")
    clear_all_users()
