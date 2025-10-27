# 🚀 START HERE - Complete Setup Guide

## ⚠️ CRITICAL: You MUST Keep 3 Terminal Windows Open

The system needs **3 separate services** running simultaneously:

```
Terminal 1: Main Backend (Port 5000)
Terminal 2: University Portal (Port 3000)  
Terminal 3: Frontend (Port 5173)
```

**If ANY of these closes, verification will fail!**

## 🎯 Quick Start (Easiest Method)

### Option 1: Use the Master Script

Open PowerShell and run:

```powershell
cd C:\Users\prash\OneDrive\Desktop\university-verifier
.\START_ALL.ps1
```

This will open 3 separate terminal windows. **DO NOT CLOSE THEM!**

### Option 2: Manual Start (More Control)

Open **3 separate PowerShell windows** and run one command in each:

**Window 1 - Main Backend:**
```powershell
cd C:\Users\prash\OneDrive\Desktop\university-verifier\backend
python run_local.py
```

**Window 2 - University Portal:**
```powershell
cd C:\Users\prash\OneDrive\Desktop\university-verifier\university-portal\backend
python app.py
```

**Window 3 - Frontend:**
```powershell
cd C:\Users\prash\OneDrive\Desktop\university-verifier\frontend
npm run dev
```

## ✅ Verify Everything is Running

```powershell
# All three should return 200 OK
curl http://localhost:5000/api/v1/health  # Backend
curl http://localhost:3000/health         # University Portal
curl http://localhost:5173                # Frontend
```

## 📋 How to Use the System

### Step 1: Open Browser
Go to: http://localhost:5173

### Step 2: Navigate to Upload
Click "Upload Certificate" in the navigation

### Step 3: Upload Your Certificate
- Choose your certificate file (PDF, JPG, PNG)
- Click "Upload Certificate"
- Wait 5-10 seconds for processing

### Step 4: See Results
You should see:
```
✅ Certificate VERIFIED
Confidence Score: 100%

Matched University Record:
- Student: Prashant Singh
- Enrollment: 231B225
- Branch: Computer Science Engineering
- CGPA: 6.1
```

## 🔴 If Verification Shows "NO" or "NOT VERIFIED"

### Check 1: Are ALL 3 Services Running?

```powershell
# Check each service
curl http://localhost:5000/api/v1/health
curl http://localhost:3000/health
curl http://localhost:5173
```

If ANY fails, that service crashed! Restart it.

### Check 2: Is Certificate in University Database?

```powershell
curl http://localhost:3000/api/certificates
```

Should show 1 certificate for enrollment 231B225.

If not, add it:
```powershell
cd university-portal
python add_certificate.py
```

### Check 3: Test Verification API Directly

```powershell
curl -Method POST -Uri "http://localhost:3000/api/verify" -ContentType "application/json" -Body '{"student_name":"Prashant Singh","enrollment_number":"231B225"}'
```

Should return `"verified": true`

## 🛠️ Common Issues

### Issue: Service keeps crashing

**Symptom**: Terminal window closes immediately

**Solution**: Check for errors in the terminal. Common causes:
- Port already in use
- Missing dependencies
- Python/Node not installed

### Issue: "Connection refused" or "Unable to connect"

**Symptom**: Services can't talk to each other

**Solution**: Make sure all 3 services are running simultaneously

### Issue: Enrollment number extracted wrong

**Symptom**: Shows different enrollment number than 231B225

**Solution**: 
1. Check if OCR is reading correctly
2. Set OpenAI API key for better extraction
3. Verify certificate image quality

### Issue: "Certificate NOT FOUND"

**Symptom**: Verification always fails

**Solution**:
1. Verify university portal is running: `curl http://localhost:3000/health`
2. Check database has certificate: `curl http://localhost:3000/api/certificates`
3. Verify enrollment number matches exactly: "231B225"

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│  User Browser                           │
│  http://localhost:5173                  │
└────────────┬────────────────────────────┘
             │ Upload Certificate
             ▼
┌─────────────────────────────────────────┐
│  Frontend (Port 5173)                   │
│  - React/Vite                           │
│  - User Interface                       │
└────────────┬────────────────────────────┘
             │ POST /api/v1/certificates/upload
             ▼
┌─────────────────────────────────────────┐
│  Main Backend (Port 5000)               │  ← MUST BE RUNNING
│  - Flask API                            │
│  - OCR + AI Extraction                  │
│  - SQLite Database                      │
└────────────┬────────────────────────────┘
             │ POST /api/verify
             ▼
┌─────────────────────────────────────────┐
│  University Portal (Port 3000)          │  ← MUST BE RUNNING
│  - Flask API                            │
│  - Certificate Database (JSON)          │
│  - Verification Logic                   │
└─────────────────────────────────────────┘
```

**ALL THREE MUST BE RUNNING FOR VERIFICATION TO WORK!**

## 🔒 Why Services Keep Stopping

Services may stop if:
1. Terminal window is closed
2. Error occurs (check terminal for errors)
3. Port conflict (another app using the port)
4. System goes to sleep
5. Ctrl+C pressed in terminal

**Solution**: Keep all 3 terminal windows open and visible!

## 💾 Database Locations

**Main App Database (SQLite)**
- Location: `backend/university.db`
- Stores: Uploaded certificates, extracted data
- Commands: SQL via Python

**University Portal Database (JSON)**
- Location: `university-portal/database/certificates.json`
- Stores: Official university records
- Commands: `python add_certificate.py` or edit JSON directly

## 🎓 Adding More Students

To add more students to the university database:

```powershell
cd university-portal
python add_certificate.py --interactive
```

Enter details when prompted.

## 📝 Testing Checklist

Before uploading:

- [ ] Backend running (port 5000)
- [ ] University portal running (port 3000)
- [ ] Frontend running (port 5173)
- [ ] Certificate in database (231B225)
- [ ] All health checks pass

## 🚨 Emergency Reset

If everything is broken:

```powershell
# Stop all services (close all terminal windows)

# Delete databases (optional)
Remove-Item backend\university.db
Remove-Item university-portal\database\certificates.json

# Re-add certificate
cd university-portal
python add_certificate.py

# Restart everything
.\START_ALL.ps1
```

## ✨ Success Indicators

You know it's working when:

1. ✅ All 3 services respond to health checks
2. ✅ Upload page loads without errors
3. ✅ Certificate uploads successfully
4. ✅ Verification shows "VERIFIED" with 100% confidence
5. ✅ Matched university record is displayed

---

**Current System Status:**
- ✅ All services restarted
- ✅ Certificate added to database
- ✅ System ready for testing

**Now try uploading your certificate again!**
