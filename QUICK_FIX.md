# Quick Fix: Certificate Verification Not Working

## Problem
Enrollment Number: **231B225** shows as **NOT VERIFIED** even though the certificate is valid.

## Root Cause
The **university portal server is not running** on port 3000. The verification system needs both:
1. ✅ Main app (port 5173) - Running
2. ❌ University portal (port 3000) - **NOT Running**

## Solution (2 Steps)

### Step 1: Start University Portal

Open a **NEW PowerShell terminal** and run:

```powershell
cd C:\Users\prash\OneDrive\Desktop\university-verifier
.\start-university-portal.ps1
```

Or manually:
```powershell
cd university-portal\backend
python app.py
```

You should see:
```
🎓 Starting JUET University Portal...
🌐 Server will run on http://localhost:3000
```

**Keep this terminal running!**

### Step 2: Re-upload Certificate

1. Go back to your main app: http://localhost:5173
2. Upload your certificate again
3. You should now see:
   - ✅ **Student Verified: YES**
   - ✅ **Enrollment Number: 231B225**
   - ✅ **Certificate Match: YES**

## Verification

Check if university portal is running:
```powershell
curl http://localhost:3000/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "JUET University Portal",
  ...
}
```

## Database Status

✅ Certificate database now contains:
- **Student Name:** Prashant Singh
- **Enrollment:** 231B225
- **Branch:** Computer Science Engineering
- **CGPA:** 6.1
- **Status:** Active

## Architecture

```
┌─────────────────────────────────────────┐
│  Certificate Verifier (Port 5173)      │
│  - Extracts certificate data with AI   │
│  - Sends to university portal for       │
│    verification                         │
└────────────────┬────────────────────────┘
                 │
                 │ POST /api/verify
                 │ {name, enrollment}
                 ▼
┌─────────────────────────────────────────┐
│  University Portal (Port 3000)          │
│  - Checks against database              │
│  - Returns verification status          │
│  - Database: university-portal/         │
│    database/certificates.json           │
└─────────────────────────────────────────┘
```

## Common Issues

### Issue: Port 3000 already in use
```powershell
# Find process using port 3000
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess

# Kill it
Stop-Process -Id <PID>
```

### Issue: Certificate not in database
```powershell
# Add certificate
python university-portal\add_certificate.py --interactive
```

### Issue: Wrong student name/enrollment
Edit the certificate in database:
```powershell
# Edit the file
notepad university-portal\database\certificates.json
```

Or add correct one:
```powershell
python university-portal\add_certificate.py --interactive
```
