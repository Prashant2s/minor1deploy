# ❌ FIX: Certificate Still Shows NOT VERIFIED

## Problem
You're seeing:
- ❌ **Student Verified: NO**
- ❌ **Enrollment Number: 231B225**
- ❌ **Certificate Match: NO**

## Root Cause Found
The **MAIN BACKEND** (port 5000) is not running! You need **THREE services** running:

```
❌ Main Backend (5000)     ← THIS IS MISSING!
✅ University Portal (3000) ← Already running
✅ Frontend (5173)          ← Already running
```

## INSTANT FIX (Choose One)

### Option 1: Start Everything At Once (EASIEST)

```powershell
.\START_ALL.ps1
```

This will open 3 new windows and start all services automatically!

### Option 2: Start Backend Manually

Open a **NEW PowerShell window** and run:

```powershell
cd C:\Users\prash\OneDrive\Desktop\university-verifier
.\start-backend.ps1
```

Or:

```powershell
cd backend
python run_local.py
```

## After Starting Backend

1. Wait 10 seconds for backend to start
2. Go to http://localhost:5173
3. Upload your certificate again
4. You should see ✅ **VERIFIED**!

## Verify All Services Running

```powershell
# Check all ports
curl http://localhost:5000/health  # Main Backend
curl http://localhost:3000/health  # University Portal  
curl http://localhost:5173         # Frontend
```

All three should respond!

## The Complete Architecture

```
┌─────────────────────────┐
│ Frontend (Port 5173)    │
│ - User Interface        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Main Backend (5000)     │ ← YOU NEED THIS!
│ - AI Extraction         │
│ - OCR Processing        │
│ - Calls University API  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ University Portal(3000) │
│ - Certificate Database  │
│ - Verification Logic    │
└─────────────────────────┘
```

## Current Status

✅ Certificate in database: **Prashant Singh (231B225)**
✅ University portal: **RUNNING**
✅ Frontend: **RUNNING**
❌ Main backend: **NOT RUNNING** ← Fix this!

## Why It's Not Working

The frontend sends requests to the main backend (port 5000), which then:
1. Extracts certificate data with AI
2. Sends verification request to university portal (port 3000)
3. Returns combined result to frontend

Without the main backend running, nothing happens!

## Quick Test After Fix

```powershell
# This should work after starting backend:
curl -Method POST -Uri "http://localhost:5000/certificates/upload" -ContentType "multipart/form-data" -InFile "your-certificate.pdf"
```
