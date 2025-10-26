# 🎓 How to Use - University Certificate Verifier

## ✅ Docker is Running!

All services are now started. Here's how to use them:

---

## 1️⃣ University Portal (Admin) - Upload Original Certificates

**URL**: http://localhost:3000/admin.html

### Admin Login:
- **Username**: `admin`
- **Password**: `admin123`

### How to Use:
1. Open http://localhost:3000/admin.html in your browser
2. Login with admin credentials
3. Fill the form with student details:
   - Student Name
   - Enrollment Number
   - Branch
   - CGPA
   - Academic Year
   - Status
4. Click "Upload Certificate"
5. Certificate is added to university database

**Purpose**: This is where the university admin uploads **ORIGINAL** certificates to the database. These will be used for verification.

---

## 2️⃣ Certificate Verifier (Student/Admin) - Test Certificates

**URL**: http://localhost:5173

### Login Options:

**Student Login:**
- **Username**: `student`
- **Password**: `student123`

**Admin Login:**
- **Username**: `admin`
- **Password**: `admin123`

### How to Use:
1. Open http://localhost:5173
2. Login with either student or admin credentials
3. Upload a certificate (PDF, JPG, PNG)
4. AI will:
   - Extract student name, enrollment, CGPA, etc.
   - Generate a summary
   - Verify against university database
5. See results with ✅ VERIFIED or ❌ NOT FOUND

**Purpose**: This is the main application where students/admins upload certificates to verify them using AI extraction and university database verification.

---

## 🔄 How Verification Works

```
Step 1: Upload Test Certificate (Port 5173)
          ↓
Step 2: AI Extracts Data (Backend Port 5000)
          ↓
Step 3: Backend Queries University Portal (Port 3000)
          ↓
Step 4: Compare with Original Database
          ↓
Step 5: Show ✅ VERIFIED or ❌ NOT FOUND
```

---

## 📊 Testing the System

### Test Scenario 1: Verify Existing Certificate

1. **First, check existing certificates in university database**:
   - Go to: http://localhost:3000/api/certificates
   - You'll see 5 sample certificates with names like:
     - Arjun Kumar Sharma (19BTCSE001)
     - Priya Singh (19BTECE002)
     - Amit Verma (18BTCSE005)

2. **Now test verification**:
   - Go to: http://localhost:5173
   - Login (student/student123 or admin/admin123)
   - Upload ANY certificate image
   - If the AI extracts a name matching the database → ✅ VERIFIED
   - If not → ❌ NOT FOUND

### Test Scenario 2: Add Your Own Certificate

1. **Upload to University Portal (Admin)**:
   - Go to: http://localhost:3000/admin.html
   - Login: admin / admin123
   - Add your certificate details (make up some data for testing)

2. **Test Verification**:
   - Go to: http://localhost:5173
   - Login
   - Upload a certificate with matching details
   - Should show ✅ VERIFIED!

---

## 🔐 Login Credentials Summary

| Service | URL | Username | Password | Purpose |
|---------|-----|----------|----------|---------|
| **University Portal** | http://localhost:3000/admin.html | admin | admin123 | Upload original certificates |
| **Certificate Verifier (Student)** | http://localhost:5173 | student | student123 | Verify certificates |
| **Certificate Verifier (Admin)** | http://localhost:5173 | admin | admin123 | Verify certificates |

---

## 📝 Sample Data in University Database

Already loaded with 5 sample certificates:

| Student Name | Enrollment | Branch | CGPA |
|--------------|------------|--------|------|
| Arjun Kumar Sharma | 19BTCSE001 | CSE | 8.75 |
| Priya Singh | 19BTECE002 | ECE | 9.12 |
| Rahul Patel | 20BTME003 | ME | 7.85 |
| Sneha Gupta | 21BTIT004 | IT | 8.95 |
| Amit Verma | 18BTCSE005 | CSE | 9.45 |

---

## 🎯 Quick Start

```bash
# 1. University Admin uploads original certificates
Open: http://localhost:3000/admin.html
Login: admin / admin123
Upload certificate details

# 2. Students verify their certificates
Open: http://localhost:5173
Login: student / student123
Upload certificate image
See AI extraction + verification result!
```

---

## 🛑 Stop Docker

```bash
docker-compose down
```

## 🔄 Restart Docker

```bash
docker-compose up -d
```

## 📋 View Logs

```bash
# All logs
docker-compose logs -f

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs university-portal
```

---

## ✨ Features

✅ **Simple Login** - Student and Admin access  
✅ **University Portal** - Admin uploads original certificates  
✅ **AI Extraction** - GPT-4o-mini extracts certificate data  
✅ **Verification** - Compares with university database  
✅ **Clean UI** - Simple and easy to use  
✅ **Logout** - Secure session management  

---

**🎉 Everything is set up and ready to use!**
