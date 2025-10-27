#!/usr/bin/env python3
"""
Script to add a certificate to the university database
"""

import json
import os
from datetime import datetime

# Database file path
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(script_dir, 'database', 'certificates.json')

def load_certificates():
    """Load certificates from database"""
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading certificates: {e}")
        return {"certificates": [], "metadata": {}}

def save_certificates(data):
    """Save certificates to database"""
    try:
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving certificates: {e}")
        return False

def generate_certificate_id(certificates):
    """Generate next certificate ID"""
    if not certificates:
        return "JUET001"
    
    max_id = 0
    for cert in certificates:
        cert_id = cert.get('id', '')
        if cert_id.startswith('JUET'):
            try:
                num = int(cert_id[4:])
                max_id = max(max_id, num)
            except ValueError:
                continue
    
    return f"JUET{str(max_id + 1).zfill(3)}"

def add_certificate(student_name, enrollment_number, branch, academic_year, cgpa="N/A", status="Active"):
    """Add a new certificate to the database"""
    
    # Load existing data
    data = load_certificates()
    certificates = data.get("certificates", [])
    
    # Generate certificate data
    cert_id = generate_certificate_id(certificates)
    current_time = datetime.utcnow().isoformat() + 'Z'
    
    # Extract branch abbreviation
    branch_abbrev = {
        'Computer Science Engineering': 'CSE',
        'Information Technology': 'IT',
        'Electronics & Communication': 'ECE',
        'Mechanical Engineering': 'ME',
        'Civil Engineering': 'CE',
        'Electrical Engineering': 'EE'
    }.get(branch, 'GEN')
    
    # Extract year from academic_year (e.g., "2019-2023" -> "2023")
    try:
        year = academic_year.split('-')[-1]
    except:
        year = '2024'
    
    cert_number = f"JUET/{branch_abbrev}/{year}/{cert_id[4:]}"
    
    new_certificate = {
        "id": cert_id,
        "student_name": student_name.strip(),
        "enrollment_number": enrollment_number.strip(),
        "registration_number": f"REG{year}{cert_id[4:]}",
        "degree": "Bachelor of Technology",
        "branch": branch,
        "university": "Jaypee University of Engineering & Technology",
        "graduation_date": f"{year}-06-15",
        "cgpa": str(cgpa),
        "academic_year": academic_year,
        "certificate_type": "Degree Certificate",
        "issue_date": current_time[:10],
        "certificate_number": cert_number,
        "status": status,
        "upload_timestamp": current_time
    }
    
    # Add the new certificate
    certificates.append(new_certificate)
    
    # Update metadata
    metadata = data.get("metadata", {})
    metadata['total_certificates'] = len(certificates)
    metadata['last_updated'] = current_time
    
    data['certificates'] = certificates
    data['metadata'] = metadata
    
    # Save to file
    if save_certificates(data):
        print(f"✅ Certificate added successfully!")
        print(f"   Certificate ID: {cert_id}")
        print(f"   Certificate Number: {cert_number}")
        print(f"   Student: {student_name}")
        print(f"   Enrollment: {enrollment_number}")
        print(f"   Total certificates in DB: {len(certificates)}")
        return True
    else:
        print("❌ Failed to save certificate to database")
        return False

if __name__ == '__main__':
    import sys
    
    print("🎓 University Certificate Database Manager")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        # Interactive mode
        print("\nEnter certificate details:")
        student_name = input("Student Name: ").strip()
        enrollment_number = input("Enrollment Number: ").strip()
        branch = input("Branch (e.g., Computer Science Engineering): ").strip()
        academic_year = input("Academic Year (e.g., 2019-2023): ").strip()
        cgpa = input("CGPA (optional, press Enter to skip): ").strip() or "N/A"
        status = input("Status (default: Active): ").strip() or "Active"
        
        if student_name and enrollment_number and branch and academic_year:
            add_certificate(student_name, enrollment_number, branch, academic_year, cgpa, status)
        else:
            print("❌ Missing required fields")
    else:
        # Quick add mode - add the sample certificate
        print("\n📝 Adding sample certificate from the uploaded image...")
        print("   (Based on typical certificate data)\n")
        
        # You can modify these values based on your actual certificate
        add_certificate(
            student_name="Prashant Singh",  # Change this to match your certificate
            enrollment_number="231B225",     # Change this to match your certificate
            branch="Computer Science Engineering",
            academic_year="2019-2023",
            cgpa="6.1",
            status="Active"
        )
        
        print("\n💡 To add more certificates interactively, run:")
        print("   python add_certificate.py --interactive")
