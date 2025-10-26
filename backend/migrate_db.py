#!/usr/bin/env python3
"""
Database migration script to add new columns to existing tables.
Run this script to update the database schema.
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

def migrate_database():
    """Add new columns to existing tables"""
    try:
        # Initialize database connection
        init_engine(settings.DB_URL)
        engine = get_engine()
        
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()
            
            try:
                # Check if users table exists, if not create it
                result = conn.execute(text("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'users'
                    );
                """))
                
                if not result.scalar():
                    logger.info("Creating users table...")
                    conn.execute(text("""
                        CREATE TABLE users (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(100) UNIQUE NOT NULL,
                            email VARCHAR(200) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            user_type VARCHAR(20) NOT NULL,
                            is_active BOOLEAN DEFAULT TRUE NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                            student_name VARCHAR(200),
                            student_reg_no VARCHAR(100) UNIQUE,
                            student_dob VARCHAR(10),
                            university_name VARCHAR(200),
                            university_code VARCHAR(50) UNIQUE
                        );
                    """))
                    
                    # Create indexes for users table
                    conn.execute(text("CREATE INDEX idx_users_username ON users (username);"))
                    conn.execute(text("CREATE INDEX idx_users_email ON users (email);"))
                    conn.execute(text("CREATE INDEX idx_users_type ON users (user_type);"))
                    conn.execute(text("CREATE INDEX idx_users_student_reg_no ON users (student_reg_no);"))
                    conn.execute(text("CREATE INDEX idx_users_university_code ON users (university_code);"))
                    
                    logger.info("Users table created successfully")
                else:
                    logger.info("Users table already exists")
                
                # Check if certificates table has new columns
                result = conn.execute(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'certificates' AND column_name = 'user_id';
                """))
                
                if not result.fetchone():
                    logger.info("Adding new columns to certificates table...")
                    
                    # Add new columns to certificates table
                    conn.execute(text("ALTER TABLE certificates ADD COLUMN user_id INTEGER;"))
                    conn.execute(text("ALTER TABLE certificates ADD COLUMN original_filename VARCHAR(255);"))
                    
                    # Add foreign key constraint
                    conn.execute(text("""
                        ALTER TABLE certificates 
                        ADD CONSTRAINT fk_certificates_user_id 
                        FOREIGN KEY (user_id) REFERENCES users(id);
                    """))
                    
                    # Create indexes
                    conn.execute(text("CREATE INDEX idx_certificates_user_id ON certificates (user_id);"))
                    
                    logger.info("New columns added to certificates table")
                else:
                    logger.info("Certificates table already has new columns")
                
                # Commit transaction
                trans.commit()
                logger.info("Database migration completed successfully!")
                
            except Exception as e:
                # Rollback on error
                trans.rollback()
                logger.error(f"Migration failed: {str(e)}")
                raise
                
    except Exception as e:
        logger.error(f"Database migration error: {str(e)}")
        raise

if __name__ == "__main__":
    migrate_database()
