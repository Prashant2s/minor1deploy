import requests
import json

# Test the extraction with a direct API call
url = "http://localhost:5000/api/v1/certificates/upload"

# Create a simple test file
test_content = b"Test certificate content"
files = {
    'file': ('test.jpg', test_content, 'image/jpeg')
}

response = requests.post(url, files=files)
print("Status Code:", response.status_code)
print("\nResponse:")
data = response.json()
print(json.dumps(data, indent=2))

# Check specific fields
if 'tabular_data' in data:
    td = data['tabular_data']
    print("\n=== Extracted Values ===")
    print(f"SGPA: {td.get('sgpa', 'NOT FOUND')}")
    print(f"CGPA: {td.get('cgpa', 'NOT FOUND')}")
    print(f"Subjects: {td.get('subjects', 'NOT FOUND')}")
    print(f"Student Name: {td.get('student_name', 'NOT FOUND')}")