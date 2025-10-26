#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '/app')

from app.services.extract import extract_fields_with_ai
import json

# Test with the exact sample text from OCR
test_text = """JAYPEE UNIVERSITY OF ENGINEERING & TECHNOLOGY-GUNA
CERTIFICATE OF ACADEMIC PERFORMANCE

Student Name: Prashant Singh
Enrollment No: 231B225
Degree: B.Tech
Branch: Computer Science & Engineering
Semester: 1
Academic Year: 2023-24

SUBJECT PERFORMANCE:
Subject Code | Subject Name | Grade | Credits
CS101 | Computer Programming | B+ | 4
MA101 | Engineering Mathematics-I | A | 4
PH101 | Engineering Physics | B | 3
CH101 | Engineering Chemistry | B+ | 3
ME101 | Engineering Mechanics | B | 3
EE101 | Basic Electrical Engineering | A- | 3

SGPA: 6.1
CGPA: 6.07
Total Credits: 20
Earned Credits: 20

Date of Birth: 15/03/2005
Graduation Date: 15/06/2027
Certificate Type: Semester Result

This certificate is issued based on the academic records maintained by the university."""

print("Testing AI extraction with sample certificate text...")
print("=" * 60)

try:
    result = extract_fields_with_ai(test_text)
    
    print("\nExtracted Fields:")
    print("-" * 40)
    
    # Check critical fields
    critical_fields = ['student_name', 'sgpa', 'cgpa', 'subjects', 'degree', 'branch']
    for field in critical_fields:
        value = result.get(field)
        print(f"{field}: {value}")
    
    print("\nAll fields:")
    print(json.dumps(result, indent=2, default=str))
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()