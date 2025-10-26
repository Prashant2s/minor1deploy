#!/usr/bin/env python3
"""
Check database schema and tables.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.session import get_engine, init_engine
from core.config import settings
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database():
    """Check database schema"""
    try:
        # Initialize database connection
        init_engine(settings.DB_URL)
        engine = get_engine()
        
        with engine.connect() as conn:
            # Check if users table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'users'
                );
            """))
            users_exists = result.scalar()
            print(f"Users table exists: {users_exists}")
            
            # Check if certificates table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'certificates'
                );
            """))
            certs_exists = result.scalar()
            print(f"Certificates table exists: {certs_exists}")
            
            if certs_exists:
                # Check certificates table columns
                result = conn.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'certificates' 
                    ORDER BY ordinal_position;
                """))
                print("\nCertificates table columns:")
                for row in result:
                    print(f"  {row[0]}: {row[1]}")
            
            if users_exists:
                # Check users table columns
                result = conn.execute(text("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' 
                    ORDER BY ordinal_position;
                """))
                print("\nUsers table columns:")
                for row in result:
                    print(f"  {row[0]}: {row[1]}")
                    
    except Exception as e:
        logger.error(f"Database check error: {str(e)}")
        raise

if __name__ == "__main__":
    check_database()
