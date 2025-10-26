"""
Migration script to add field_type column to extracted_fields table
Run this on your Render PostgreSQL database
"""
import os
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    exit(1)

print(f"Connecting to database...")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Check if column exists
        check_query = text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='extracted_fields' 
            AND column_name='field_type';
        """)
        result = conn.execute(check_query)
        exists = result.fetchone() is not None
        
        if exists:
            print("✅ Column 'field_type' already exists")
        else:
            print("Adding 'field_type' column...")
            # Add the column with default value
            alter_query = text("""
                ALTER TABLE extracted_fields 
                ADD COLUMN field_type VARCHAR(50) DEFAULT 'extracted' NOT NULL;
            """)
            conn.execute(alter_query)
            conn.commit()
            print("✅ Successfully added 'field_type' column")
            
            # Create index
            print("Creating index on field_type...")
            index_query = text("""
                CREATE INDEX IF NOT EXISTS idx_extracted_fields_type 
                ON extracted_fields(field_type);
            """)
            conn.execute(index_query)
            conn.commit()
            print("✅ Successfully created index")
        
        print("\n✅ Migration completed successfully!")
        
except Exception as e:
    print(f"❌ Migration failed: {str(e)}")
    exit(1)
