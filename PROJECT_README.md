# 🎓 AI-Powered University Certificate Verifier

A comprehensive AI-powered certificate verification system that uses OpenAI GPT-4o-mini for intelligent document processing, advanced OCR for text extraction, and university database verification. Built as a full-stack application with React frontend, Flask backend, and PostgreSQL database.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Deployment Guide](#deployment-guide)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

The **AI-Powered University Certificate Verifier** is an intelligent document processing system designed to:
- Extract structured data from academic certificates using AI
- Verify certificate authenticity against university databases
- Provide a modern web interface for certificate upload and management
- Generate professional AI summaries of certificate contents

This project demonstrates modern software engineering practices including:
- Full-stack web development with React and Flask
- AI integration with OpenAI API
- Database design and management
- Docker containerization
- Production deployment strategies

---

## ✨ Key Features

### AI-Powered Processing
- **OpenAI GPT-4o-mini Integration**: Intelligent field extraction and data structuring
- **Advanced OCR**: EasyOCR with image preprocessing for optimal text recognition
- **Pytesseract Support**: Additional OCR engine for enhanced accuracy
- **Smart Field Recognition**: Extracts 16+ fields including names, grades, CGPA, subjects
- **AI-Generated Summaries**: Professional, concise certificate summaries

### Data Extraction Capabilities
- **Student Information**: Name, enrollment number, registration number
- **Academic Details**: Degree, branch, university name, graduation date
- **Performance Metrics**: CGPA, SGPA, semester-wise grades
- **Subject-wise Data**: Course codes, names, grades, and credits
- **Certificate Metadata**: Certificate type, issue date, certificate number

### University Verification System
- **Database Integration**: Separate university portal with certificate database
- **Real-time Verification**: Compare extracted data with university records
- **Certificate Status**: Track and update certificate verification status
- **API Integration**: RESTful communication between systems

### Modern Web Interface
- **React 19**: Latest React version with Vite for fast development
- **Material-UI**: Professional, responsive UI components
- **Drag-and-Drop Upload**: Easy certificate file upload
- **Real-time Processing**: Live feedback during AI extraction
- **Certificate Gallery**: View and manage all uploaded certificates

### Multi-Format Support
- **Documents**: PDF files (via PyMuPDF)
- **Images**: JPG, JPEG, PNG, TIFF, BMP, WEBP
- **Size Limit**: Up to 10MB per file (configurable)
- **Batch Processing**: Support for multiple certificate uploads

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                          │
│              (React 19 + Material-UI)                       │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     │
┌────────────────────▼────────────────────────────────────────┐
│                Flask Backend API                            │
│              (Python 3.9+ / Flask 3.0.3)                    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Image      │  │   OCR        │  │   OpenAI     │     │
│  │ Preprocessing│─▶│   Service    │─▶│  Extraction  │     │
│  │  (OpenCV)    │  │  (EasyOCR)   │  │  (GPT-4o)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         SQLAlchemy ORM + Database Models             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐     ┌────────▼───────────┐
│   PostgreSQL     │     │  University Portal │
│    Database      │     │   (Flask + JSON)   │
│ (Certificates)   │     │  (Verification DB) │
└──────────────────┘     └────────────────────┘
```

### Component Breakdown

1. **Frontend Layer**
   - React-based single-page application
   - Material-UI components for consistent design
   - Axios for API communication
   - React Router for navigation

2. **Backend API Layer**
   - Flask REST API with CORS support
   - SQLAlchemy ORM for database operations
   - Image processing pipeline (OpenCV + Pillow)
   - OCR engine integration (EasyOCR + Pytesseract)

3. **AI Processing Layer**
   - OpenAI API client for field extraction
   - Prompt engineering for structured data
   - Confidence scoring for extractions
   - Summary generation

4. **Data Layer**
   - PostgreSQL for production (via Docker)
   - SQLite for local development
   - University portal with separate JSON database

5. **Deployment Layer**
   - Docker Compose for multi-container orchestration
   - Netlify for frontend hosting
   - Heroku/Railway/Render for backend hosting

---

## 🛠️ Technology Stack

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19.1.1 | UI framework for building interactive interfaces |
| **Vite** | 7.1.2 | Fast build tool and development server |
| **Material-UI** | 7.3.1 | Professional React UI component library |
| **React Router DOM** | 7.8.0 | Client-side routing and navigation |
| **Axios** | 1.11.0 | HTTP client for API communication |
| **Emotion** | 11.14.0 | CSS-in-JS styling library |
| **ESLint** | 9.33.0 | Code quality and linting |

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Flask** | 3.0.3 | Web framework for Python API |
| **SQLAlchemy** | 2.0.31 | SQL toolkit and ORM |
| **PostgreSQL** | 15 | Relational database (production) |
| **Psycopg2** | 2.9.9 | PostgreSQL adapter for Python |
| **OpenAI API** | 1.30.0 | AI-powered text extraction and summarization |
| **Pytesseract** | 0.3.13 | OCR engine for text recognition |
| **PyMuPDF** | 1.24.10 | PDF processing and text extraction |
| **Pillow** | 10.4.0 | Image manipulation and processing |
| **OpenCV** | - | Image preprocessing (via dependencies) |
| **Flask-CORS** | 4.0.0 | Cross-origin resource sharing |
| **Gunicorn** | 21.2.0 | Production WSGI server |
| **PyJWT** | 2.8.0 | JSON Web Token implementation |
| **Python-dotenv** | 1.0.0 | Environment variable management |

### University Portal Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| **Flask** | 2.3.2 | Web framework for portal API |
| **Flask-CORS** | 4.0.0 | CORS support for API |
| **JSON Database** | - | File-based certificate storage |
| **Gunicorn** | 21.2.0 | Production WSGI server |

### DevOps & Deployment

| Technology | Purpose |
|------------|---------|
| **Docker** | Container platform for consistent environments |
| **Docker Compose** | Multi-container orchestration |
| **PostgreSQL (Docker)** | Production database in container |
| **Netlify** | Frontend static site hosting |
| **Heroku/Railway/Render** | Backend API hosting options |

### AI & Machine Learning

| Technology | Purpose |
|------------|---------|
| **OpenAI GPT-4o-mini** | Large language model for text extraction |
| **EasyOCR** | Neural network-based OCR engine |
| **Pytesseract** | Traditional OCR for fallback |
| **NumPy** | Numerical computing for image processing |

---

## 📁 Project Structure

```
university-verifier/
│
├── backend/                          # Flask Backend API
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py            # REST API endpoints
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py            # Configuration management
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # SQLAlchemy models
│   │   │   └── session.py           # Database session management
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── extract.py           # OpenAI extraction service
│   │   │   ├── ocr.py               # OCR service (EasyOCR/Tesseract)
│   │   │   └── images.py            # Image preprocessing
│   │   └── main.py                  # Flask app factory
│   ├── uploads/                     # Uploaded certificate files
│   ├── requirements.txt             # Python dependencies
│   ├── run_local.py                 # Local development server
│   ├── wipe_certs.py               # Database cleanup utility
│   ├── check_db.py                  # Database inspection tool
│   ├── migrate_db.py                # Database migration script
│   └── university.db                # SQLite database (local dev)
│
├── frontend/                         # React Frontend Application
│   ├── public/
│   │   ├── juet-official-logo.png   # University logo
│   │   └── vite.svg                 # Vite logo
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js             # API client configuration
│   │   ├── pages/
│   │   │   ├── Upload.jsx           # Certificate upload page
│   │   │   ├── Records.jsx          # All certificates list
│   │   │   ├── RecordDetail.jsx     # Certificate detail view
│   │   │   └── MyCertificates.jsx   # User's certificates
│   │   ├── App.jsx                  # Main app component
│   │   ├── App.css                  # Application styles
│   │   └── main.jsx                 # React entry point
│   ├── dist/                        # Production build output
│   ├── package.json                 # Node.js dependencies
│   ├── package-lock.json            # Locked dependency versions
│   ├── vite.config.js              # Vite configuration
│   └── eslint.config.js            # ESLint configuration
│
├── university-portal/               # Separate University Database Portal
│   ├── backend/
│   │   ├── app.py                  # Flask portal API
│   │   └── requirements.txt        # Portal dependencies
│   ├── database/
│   │   └── certificates.json       # University certificate database
│   ├── frontend/                   # Portal frontend (if any)
│   └── Dockerfile                  # Portal container config
│
├── docker/                          # Docker Configuration Files
│   ├── backend.Dockerfile          # Backend container build
│   └── frontend.Dockerfile         # Frontend container build
│
├── .venv/                           # Python virtual environment (local)
├── uploads/                         # Root uploads directory
├── extracted_data/                  # Extracted certificate data
│   └── sample_certificates.json    # Sample data for testing
│
├── docker-compose.yml              # Multi-container orchestration
├── .env                            # Environment variables (gitignored)
├── .env.example                    # Environment template
├── env.example                     # Alternative env template
├── env.production                  # Production env template
│
├── deploy.bat                      # Windows deployment script
├── deploy.sh                       # Linux/Mac deployment script
├── quick-refresh.bat               # Quick Docker refresh (Windows)
├── refresh-docker.bat              # Full Docker refresh (Windows)
├── refresh-docker.ps1              # Docker refresh (PowerShell)
├── run-both-systems.ps1            # Run both systems (PowerShell)
│
├── netlify.toml                    # Netlify deployment config
├── Procfile                        # Heroku deployment config
├── runtime.txt                     # Python runtime version
│
├── .gitignore                      # Git ignore rules
├── README.md                       # Original README
├── QUICKSTART.md                   # Quick setup guide
├── SIMPLE_SETUP.md                 # Simplified setup guide
├── DEPLOYMENT_GUIDE.md             # Detailed deployment guide
├── DEPLOYMENT_CHECKLIST.md         # Deployment checklist
├── DEPLOYMENT_READY.md             # Pre-deployment verification
└── README_DEPLOYMENT.md            # Deployment-specific README
```

---

## 📋 Prerequisites

### Required Software

1. **Docker & Docker Compose**
   - Docker Desktop 20.10+ (includes Docker Compose)
   - Ensures consistent environment across all platforms
   - Download: https://www.docker.com/products/docker-desktop

2. **OpenAI API Key** (REQUIRED)
   - This is an AI-powered application that requires OpenAI API access
   - Get your key: https://platform.openai.com/api-keys
   - Requires active OpenAI account with available credits

3. **Git**
   - Version control for code management
   - Download: https://git-scm.com/downloads

### Optional (For Local Development)

4. **Node.js 18+**
   - Required for frontend development outside Docker
   - Download: https://nodejs.org/

5. **Python 3.9+**
   - Required for backend development outside Docker
   - Download: https://www.python.org/downloads/

6. **PostgreSQL 15+**
   - Required for local database development
   - Included in Docker setup
   - Download: https://www.postgresql.org/download/

### System Requirements

- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for Docker images and data
- **OS**: Windows 10/11, macOS 10.15+, or Linux
- **Internet**: Required for API calls and package downloads

---

## 🚀 Installation & Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <repository-url>
cd university-verifier
```

### Step 2: Set Up Environment Variables

```bash
# Copy the environment template
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux/Mac
cp .env.example .env
```

### Step 3: Configure Environment Variables

Edit the `.env` file with your actual values:

```env
# AI Configuration - REQUIRED
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_BASE_URL=

# Database Configuration
POSTGRES_PASSWORD=your_secure_password_here
DB_URL=postgresql://postgres:your_postgres_password@localhost:5432/university_verifier

# University Portal URL (auto-configured in Docker)
UNIVERSITY_PORTAL_URL=http://university-portal:3000

# Application Configuration
CORS_ORIGIN=http://localhost:3000,http://localhost:5173
UPLOAD_DIR=./uploads

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here

# Deployment Configuration
PORT=5000
HOST=0.0.0.0
```

**Important Notes:**
- `OPENAI_API_KEY` is **mandatory** - the application will not work without it
- Generate a strong password for `POSTGRES_PASSWORD`
- `CORS_ORIGIN` should include all frontend URLs (comma-separated)
- Keep the `.env` file secure and never commit it to version control

### Step 4: Verify Docker Installation

```bash
# Check Docker version
docker --version
# Should output: Docker version 20.10+ or higher

# Check Docker Compose version
docker-compose --version
# Should output: docker-compose version 2.0+ or higher

# Test Docker is running
docker ps
# Should show a list of containers (may be empty)
```

---

## 🎮 Running the Application

### Option 1: Using Docker Compose (Recommended)

#### Windows

```powershell
# Full deployment with automatic build
.\deploy.bat

# Or using PowerShell script
.\run-both-systems.ps1

# Manual Docker Compose
docker-compose --env-file .env up --build
```

#### Linux/Mac

```bash
# Make scripts executable
chmod +x deploy.sh

# Run deployment
./deploy.sh

# Or manual Docker Compose
docker-compose --env-file .env up --build
```

#### What Gets Started:

1. **PostgreSQL Database** (port 5432)
   - Production database for certificates
   - Persistent volume for data storage

2. **Backend API** (port 5000)
   - Flask application with AI processing
   - Accessible at: http://localhost:5000

3. **Frontend Application** (port 5173)
   - React web interface
   - Accessible at: http://localhost:5173

4. **University Portal** (port 3000)
   - Separate university database portal
   - Accessible at: http://localhost:3000

### Option 2: Local Development (Without Docker)

#### Backend Development

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run_local.py
```

Backend will run on http://localhost:5000

#### Frontend Development

```bash
# Navigate to frontend directory (new terminal)
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will run on http://localhost:5173

#### University Portal

```bash
# Navigate to portal directory (new terminal)
cd university-portal/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run portal server
python app.py
```

Portal will run on http://localhost:3000

---

## 📊 Using the Application

### 1. Upload a Certificate

1. Open http://localhost:5173 in your browser
2. Click **"Upload"** or **"AI Certificate Verifier"** in navigation
3. Drag and drop a certificate image/PDF or click to browse
4. Wait for AI processing (typically 10-30 seconds)
5. View extracted data and AI summary

### 2. View All Certificates

1. Click **"All Records"** in navigation
2. Browse all uploaded certificates
3. Click on any certificate to view details

### 3. View Your Certificates

1. Click **"My Certificates"** in navigation
2. View certificates uploaded in current session
3. Search and filter by various fields

### 4. Verify Certificate

1. Open a certificate detail page
2. Click **"Verify with University Database"**
3. System compares with university portal data
4. View verification status and confidence score

---

## 🔌 API Documentation

### Base URL

```
Local: http://localhost:5000/api/v1
Production: https://your-backend-url.com/api/v1
```

### Authentication

Currently, the API does not require authentication. For production, implement JWT authentication.

### Endpoints

#### 1. Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Upload Certificate

```http
POST /api/v1/certificates/upload
Content-Type: multipart/form-data
```

**Request Body:**
```
file: <certificate-file> (PDF, JPG, PNG, etc.)
```

**Response:**
```json
{
  "id": 1,
  "filename": "certificate.pdf",
  "upload_date": "2024-01-15T10:30:00Z",
  "extracted_data": {
    "student_name": "John Doe",
    "enrollment_number": "12345678",
    "degree": "B.Tech",
    "branch": "Computer Science & Engineering",
    "university": "Example University",
    "cgpa": "8.5",
    "graduation_date": "15/06/2023",
    "subjects": [
      {
        "code": "CS101",
        "name": "Programming Fundamentals",
        "grade": "A",
        "credits": 4
      }
    ]
  },
  "ai_summary": "Student John Doe completed B.Tech in Computer Science with CGPA 8.5...",
  "confidence_score": 0.95,
  "processing_time": 15.3
}
```

#### 3. Get All Certificates

```http
GET /api/v1/certificates
```

**Response:**
```json
{
  "certificates": [
    {
      "id": 1,
      "filename": "certificate.pdf",
      "upload_date": "2024-01-15T10:30:00Z",
      "student_name": "John Doe",
      "enrollment_number": "12345678"
    }
  ],
  "total": 1
}
```

#### 4. Get Certificate by ID

```http
GET /api/v1/certificates/{id}
```

**Response:**
```json
{
  "id": 1,
  "filename": "certificate.pdf",
  "upload_date": "2024-01-15T10:30:00Z",
  "extracted_data": { ... },
  "ai_summary": "...",
  "confidence_score": 0.95
}
```

#### 5. Get Certificate Image

```http
GET /api/v1/certificates/{id}/image
```

**Response:** Binary image data

### University Portal API

#### Base URL

```
Local: http://localhost:3000/api
Docker: http://university-portal:3000/api
```

#### 1. Get All Certificates

```http
GET /api/certificates
```

#### 2. Add Certificate

```http
POST /api/certificates
Content-Type: application/json
```

**Request Body:**
```json
{
  "student_name": "John Doe",
  "enrollment_number": "12345678",
  "branch": "Computer Science Engineering",
  "cgpa": 8.5,
  "academic_year": "2019-2023",
  "status": "verified"
}
```

#### 3. Verify Certificate

```http
POST /api/verify
Content-Type: application/json
```

**Request Body:**
```json
{
  "enrollment_number": "12345678",
  "student_name": "John Doe",
  "cgpa": "8.5"
}
```

---

## 🚢 Deployment Guide

### Frontend Deployment (Netlify)

#### Prerequisites
- Netlify account (free tier available)
- GitHub repository connected to Netlify

#### Steps

1. **Update Backend URL in Frontend**

```bash
# Edit frontend/src/api/axios.js
const API_URL = 'https://your-backend-url.com/api/v1';
```

2. **Update Netlify Configuration**

Edit `netlify.toml`:
```toml
[build]
  command = "cd frontend && npm install && npm run build"
  publish = "frontend/dist"

[build.environment]
  NODE_VERSION = "18"
  VITE_API_URL = "https://your-backend-url.com/api/v1"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

3. **Deploy to Netlify**

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy
netlify deploy --prod
```

Or use Netlify web interface:
1. Connect GitHub repository
2. Configure build settings
3. Deploy automatically

### Backend Deployment Options

#### Option 1: Heroku

```bash
# Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:essential-0

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key
heroku config:set POSTGRES_PASSWORD=your_password
heroku config:set CORS_ORIGIN=https://your-frontend.netlify.app

# Deploy
git push heroku main

# Check logs
heroku logs --tail
```

#### Option 2: Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Add PostgreSQL database
5. Set environment variables in Railway dashboard:
   - `OPENAI_API_KEY`
   - `POSTGRES_PASSWORD`
   - `CORS_ORIGIN`
6. Railway will automatically build and deploy

#### Option 3: Render

1. Go to [Render.com](https://render.com)
2. Click **"New"** → **"Web Service"**
3. Connect GitHub repository
4. Configure build settings:
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn app.main:app`
5. Add PostgreSQL database
6. Set environment variables in Render dashboard
7. Deploy

#### Option 4: DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub
3. Select backend folder as root directory
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `gunicorn app.main:app`
5. Add managed PostgreSQL database
6. Set environment variables
7. Deploy

### University Portal Deployment

The university portal can be deployed separately or as part of the main Docker Compose stack.

#### Standalone Deployment

```bash
# Navigate to portal directory
cd university-portal

# Build Docker image
docker build -t university-portal .

# Run container
docker run -p 3000:3000 -v $(pwd)/database:/app/database university-portal
```

### Environment Variables for Production

```env
# Backend
OPENAI_API_KEY=your_openai_api_key
POSTGRES_PASSWORD=strong_password
DB_URL=postgresql://user:password@host:port/database
CORS_ORIGIN=https://your-frontend-url.com
MAX_FILE_SIZE=10485760
LOG_LEVEL=INFO

# Frontend
VITE_API_URL=https://your-backend-url.com/api/v1
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 1. Docker Container Fails to Start

**Symptoms:**
- Containers exit immediately
- Error messages in logs

**Solutions:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up

# Check if ports are already in use
# Windows
netstat -ano | findstr :5000
netstat -ano | findstr :5173

# Linux/Mac
lsof -i :5000
lsof -i :5173
```

#### 2. OpenAI API Errors

**Symptoms:**
- "API key missing" error
- "Insufficient credits" error
- Slow or failed extractions

**Solutions:**
- Verify API key is correctly set in `.env`
- Check OpenAI API credits: https://platform.openai.com/usage
- Test API key:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

#### 3. Database Connection Errors

**Symptoms:**
- "Connection refused" errors
- "Table does not exist" errors

**Solutions:**
```bash
# Check if PostgreSQL container is running
docker ps | grep postgres

# Restart database container
docker-compose restart db

# Check database logs
docker-compose logs db

# Verify connection string in .env
# Format: postgresql://user:password@host:port/database
```

#### 4. CORS Errors

**Symptoms:**
- "Blocked by CORS policy" in browser console
- API requests fail from frontend

**Solutions:**
- Update `CORS_ORIGIN` in `.env` to include frontend URL
- Restart backend after changing environment variables
- Check frontend is making requests to correct backend URL

#### 5. File Upload Issues

**Symptoms:**
- "File too large" errors
- Upload hangs or fails
- "Unsupported file type" errors

**Solutions:**
```env
# Increase max file size in .env
MAX_FILE_SIZE=20971520  # 20MB

# Verify file format is supported
# Supported: PDF, JPG, JPEG, PNG, TIFF, BMP, WEBP
```

#### 6. Slow AI Processing

**Symptoms:**
- Extractions take very long
- Timeout errors

**Solutions:**
- Optimize image before upload (reduce resolution)
- Check internet connection speed
- Verify OpenAI API status: https://status.openai.com
- Consider using faster OpenAI model in `extract.py`

#### 7. Frontend Not Loading

**Symptoms:**
- Blank page in browser
- 404 errors for assets

**Solutions:**
```bash
# Clear browser cache
# Rebuild frontend
cd frontend
npm run build

# Check Vite configuration
# Verify VITE_API_URL in .env or netlify.toml
```

### Logs and Debugging

#### Docker Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
docker-compose logs university-portal

# View last 100 lines
docker-compose logs --tail=100
```

#### Local Development Logs

```bash
# Backend logs (run_local.py)
# Output shows in terminal where you ran python run_local.py

# Frontend logs
# Browser DevTools → Console tab
# Network tab for API requests

# Check Flask debug output
# Enable debug mode in run_local.py
```

### Performance Optimization

#### Image Processing

```python
# Optimize images before upload (frontend)
# Consider resizing large images to max 2000px width
# Use WebP format for better compression
```

#### Database

```sql
-- Add indexes for frequently queried fields
CREATE INDEX idx_enrollment ON certificates(enrollment_number);
CREATE INDEX idx_upload_date ON certificates(upload_date);
```

#### Caching

```python
# Implement caching for repeated extractions
# Use Redis or in-memory cache for API responses
```

---

## 🤝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Write meaningful commit messages

4. **Test your changes**
```bash
# Test backend
cd backend
pytest

# Test frontend
cd frontend
npm run lint
npm run build
```

5. **Commit changes**
```bash
git add .
git commit -m "Add: description of your feature"
```

6. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

7. **Submit a Pull Request**
   - Provide clear description
   - Reference any related issues
   - Wait for code review

### Code Style Guidelines

#### Python (Backend)

```python
# Follow PEP 8
# Use type hints
def process_image(image_path: str) -> dict:
    """
    Process certificate image and extract text.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing extracted data
    """
    pass

# Use meaningful variable names
# Add docstrings to functions
# Handle exceptions gracefully
```

#### JavaScript/React (Frontend)

```javascript
// Use ESLint configuration
// Follow React best practices
// Use functional components with hooks

// Use meaningful component names
const CertificateUpload = () => {
  // Component logic
};

// Add prop types or TypeScript
// Write clean, readable code
```

### Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd frontend
npm test

# Docker integration tests
docker-compose -f docker-compose.test.yml up
```

---

## 📄 License

This project is developed for educational purposes as part of a university project.

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-4o-mini API
- **EasyOCR** for OCR capabilities
- **Flask** and **React** communities
- **Material-UI** for UI components
- **Docker** for containerization

---

## 📞 Support & Contact

For questions, issues, or contributions:

1. **Check Documentation**: Review this README and other documentation files
2. **GitHub Issues**: Open an issue for bugs or feature requests
3. **Logs**: Check Docker logs for detailed error messages
4. **API Testing**: Use Postman or curl to test API endpoints

---

## 🎯 Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement certificate templates
- [ ] Add bulk certificate upload
- [ ] Support for more document formats
- [ ] Real-time WebSocket updates
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Blockchain integration for verification
- [ ] Multi-language support
- [ ] Advanced search and filtering

---

**Built with ❤️ for educational purposes | AI-Powered Certificate Verification System**
