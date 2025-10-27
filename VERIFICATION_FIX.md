# Certificate Verification Fix

## Problem
The certificate verification was showing "Certificate NOT FOUND in University Database" with 0% confidence even when the certificate data matched the university records.

## Root Cause
**The university portal database was empty!**

Looking at `university-portal/database/certificates.json`, it has:
```json
{
  "certificates": [],
  "metadata": {
    "total_certificates": 0,
    ...
  }
}
```

## Solution

### Step 1: Add Certificate to University Database

Run the script to add your certificate to the university database:

```powershell
cd university-portal
python add_certificate.py
```

By default, this adds a sample certificate. **You need to edit the script** to match YOUR actual certificate details:

Edit `university-portal/add_certificate.py` lines 146-152:
```python
add_certificate(
    student_name="Your Name Here",      # ⬅️ Change this
    enrollment_number="Your Enroll#",   # ⬅️ Change this
    branch="Computer Science Engineering",
    academic_year="2019-2023",         # ⬅️ Change if needed
    cgpa="6.1",                        # ⬅️ Change if needed
    status="Active"
)
```

### Step 2: Run University Portal

Make sure the university portal is running on port 3000:

```powershell
cd university-portal\backend
python app.py
```

You should see:
```
🎓 Starting JUET University Portal...
🌐 Server will run on http://localhost:3000
```

### Step 3: Test Verification

Now upload your certificate again in the main verifier app (port 5173), and it should show:
- ✅ Certificate VERIFIED
- Confidence Score: 100%

## Improvements Made

I've also improved the verification matching logic in `university-portal/backend/app.py`:

1. **Normalization**: Removes extra spaces, special characters, and makes comparison case-insensitive
2. **Better Matching**: Prioritizes enrollment number (unique identifier) over name matching
3. **Confidence Scoring**: Returns different confidence scores based on match quality:
   - 1.0 (100%) - Perfect match on both name and enrollment
   - 0.9 (90%) - Enrollment matches but name differs slightly
   - 0.7 (70%) - Name matches but enrollment differs
4. **Logging**: Added detailed logs to help debug matching issues

## Interactive Mode

To add multiple certificates interactively:

```powershell
cd university-portal
python add_certificate.py --interactive
```

Then enter details when prompted.

## Verify Database Contents

To check what certificates are in the database:

```powershell
# View the database file
cat university-portal\database\certificates.json

# Or use the API
curl http://localhost:3000/api/certificates
```

## Alternative: Use University Portal Admin UI

The university portal also has an admin interface where you can add certificates:

1. Open http://localhost:3000/admin.html
2. Login or register as university admin
3. Add certificates through the web interface

## Key Takeaway

The verification system requires **two-way setup**:
1. ✅ Main verifier extracts certificate data (working)
2. ❌ University database must contain matching records (was missing)

Both systems need to be running and properly configured for verification to work!
