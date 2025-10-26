# Certificate Verification Workflow

## Overview
The system now has two main components that work together:

### 1. **University Portal (Admin Side)** - Port 3000
- **Purpose**: Store original/authentic certificates from the university
- **URL**: http://localhost:3000/admin.html
- **Functionality**: 
  - Admin uploads the **actual certificate file** (PDF/JPG/PNG)
  - Along with student details (name, enrollment number, branch, academic year, status)
  - Certificates are stored in the university database as the "source of truth"

### 2. **Certificate Verifier (User Side)** - Port 5173
- **Purpose**: Verify uploaded certificates against university database
- **URL**: http://localhost:5173
- **Functionality**:
  - Users upload certificates they want to verify
  - AI extracts data from the certificate (name, enrollment, branch, etc.)
  - System compares extracted data with university portal database
  - Shows verification status: ✓ Verified or ✗ Not Found

## How It Works

### Step 1: Admin Adds Certificate to University Portal
1. Go to http://localhost:3000/admin.html
2. Login with any alphanumeric username
3. Upload certificate with details:
   - **Certificate File** (PDF/JPG/PNG) - Required
   - Student Name - e.g., "Prashant Singh"
   - Enrollment Number - e.g., "231B225"
   - Branch - e.g., "Computer Science Engineering"
   - Academic Year - e.g., "2019-2023"
   - Status - "Valid" or "Graduated"
4. Click "Upload Certificate"
5. Certificate is now stored in university database

### Step 2: User Verifies Certificate
1. User goes to http://localhost:5173 (Certificate Verifier)
2. Uploads a certificate file
3. AI processes the certificate:
   - Extracts text using OCR
   - Uses OpenAI to identify student name, enrollment number, branch, etc.
   - Formats data in tabular format
4. System automatically calls university portal API
5. Compares extracted data with university database
6. Shows verification result:
   - **✓ Verified**: Certificate found in university database
   - **✗ Not Verified**: Certificate not found or data mismatch
   - **Confidence Score**: How closely the data matches

## API Integration

### University Portal API
- **Endpoint**: `http://localhost:3000/api/verify`
- **Method**: POST
- **Request Body**:
```json
{
  "student_name": "Prashant Singh",
  "enrollment_number": "231B225"
}
```
- **Response**:
```json
{
  "success": true,
  "verified": true,
  "confidence_score": 1.0,
  "matched_certificate": {
    "student_name": "Prashant Singh",
    "enrollment_number": "231B225",
    "branch": "Computer Science Engineering",
    "status": "Graduated",
    "certificate_number": "JUET/CSE/2023/001"
  }
}
```

## File Storage

### University Portal
- Certificate files stored in: `university-portal/database/certificates/`
- Filename format: `{enrollment_number}_{cert_id}.{extension}`
- Example: `231B225_JUET001.pdf`

### Certificate Verifier
- Uploaded files stored in: `uploads/`
- Temporary storage for processing

## Benefits

1. **Authenticity**: Only certificates uploaded by university admin are considered valid
2. **Automation**: AI extracts data automatically, no manual entry needed
3. **Verification**: Instant verification against official university database
4. **Audit Trail**: All certificates stored with timestamp and metadata
5. **Confidence Scoring**: Shows how well extracted data matches official records

## Testing the System

### Test Scenario
1. **Upload to University Portal**:
   - Go to http://localhost:3000/admin.html
   - Login as "admin"
   - Upload a test certificate with:
     - Name: "Prashant Singh"
     - Enrollment: "231B225"
     - Branch: "Computer Science Engineering"
     - Year: "2019-2023"
     - Status: "Graduated"

2. **Verify on Main App**:
   - Go to http://localhost:5173
   - Upload the same certificate file
   - AI will extract the data
   - System will verify against university portal
   - Should show "✓ Verified" with match details

## Database Structure

### University Portal Database
Location: `university-portal/database/certificates.json`

```json
{
  "certificates": [
    {
      "id": "JUET001",
      "student_name": "Prashant Singh",
      "enrollment_number": "231B225",
      "branch": "Computer Science Engineering",
      "academic_year": "2019-2023",
      "status": "Graduated",
      "certificate_file": "231B225_JUET001.pdf",
      "certificate_number": "JUET/CSE/2023/001",
      "upload_timestamp": "2025-10-26T12:00:00Z"
    }
  ]
}
```

## Security Considerations

1. **Admin Access**: Only authorized admins can upload to university portal
2. **File Validation**: Only PDF, JPG, PNG files allowed (max 10MB)
3. **Duplicate Prevention**: Same enrollment number cannot be uploaded twice
4. **Data Verification**: Two-factor verification (name + enrollment match required)

## Troubleshooting

### Certificate Not Verified
- Ensure certificate was uploaded to university portal first
- Check enrollment number matches exactly
- Check student name spelling matches exactly
- View university portal database at: http://localhost:3000/api/certificates

### File Upload Failed
- Check file size (max 10MB)
- Check file format (PDF, JPG, PNG only)
- Check Docker containers are running: `docker-compose ps`

### API Connection Error
- Ensure university portal is running on port 3000
- Check backend environment variable: `UNIVERSITY_PORTAL_URL=http://university-portal:3000`
- View logs: `docker-compose logs university-portal`

## Ports
- **Frontend (Verifier)**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **University Portal**: http://localhost:3000
- **Database**: PostgreSQL on port 5432
