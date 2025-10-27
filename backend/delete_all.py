import sqlite3
import os

# Database path - check both locations
db_paths = [
    'university.db',
    '../university.db',
    os.path.join(os.path.dirname(__file__), '..', 'university.db')
]

db_path = None
for path in db_paths:
    if os.path.exists(path):
        db_path = path
        break

if not db_path:
    print("Database not found!")
    exit(1)

print(f"Using database: {os.path.abspath(db_path)}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f"\nTables in database: {tables}")

# Count certificates
if 'certificates' in tables:
    cursor.execute('SELECT COUNT(*) FROM certificates')
    cert_count = cursor.fetchone()[0]
    print(f"Found {cert_count} certificates")
    
    if cert_count > 0:
        confirm = input("\nAre you sure you want to delete ALL certificates? (yes/no): ")
        if confirm.lower() == 'yes':
            # Delete extracted fields first (foreign key)
            if 'extracted_fields' in tables:
                cursor.execute('DELETE FROM extracted_fields')
                print(f"Deleted extracted fields")
            
            # Delete certificates
            cursor.execute('DELETE FROM certificates')
            conn.commit()
            print(f"✓ Successfully deleted {cert_count} certificates!")
        else:
            print("Operation cancelled")
    else:
        print("No certificates to delete")
else:
    print("Certificates table does not exist")

conn.close()
