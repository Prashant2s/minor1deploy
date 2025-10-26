# 🎓 AI-Powered University Certificate Verifier

Complete AI-powered certificate verification system with intelligent extraction, university database verification, and multi-service architecture.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deployable-green)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

### Core Functionality
- 🤖 **AI-Powered Extraction** - Uses OpenAI GPT-4o-mini for intelligent field extraction
- 📄 **Multi-Format Support** - Handles PDF, JPG, PNG, TIFF, BMP, WEBP
- 🔍 **OCR Processing** - Advanced text recognition with EasyOCR
- ✅ **University Verification** - Matches against university database records
- 📊 **Structured Data** - Extracts 16+ fields in tabular format
- 📝 **AI Summaries** - Generates professional certificate summaries
- 💾 **Multi-Certificate Support** - Handle multiple certificates per student
- 📥 **Download & Export** - Download original files or export data as JSON

### User Features
- 🖼️ **Drag & Drop Upload** - Easy certificate upload interface
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎨 **Modern UI** - Clean, intuitive user interface
- 🔐 **Secure** - Environment-based secrets, no hardcoded credentials
- 🚀 **Fast** - Optimized for performance

### Admin Features (University Portal)
- 👥 **Student Management** - Add/edit student records
- 📋 **Certificate Records** - View all uploaded certificates
- ✅ **Status Management** - Mark certificates as Valid/Graduated
- 🔍 **Search & Filter** - Find students by enrollment number

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                                                      │
│  ┌──────────────┐         ┌──────────────┐         │
│  │   Frontend   │────────▶│  Backend API │         │
│  │   (React)    │         │   (Flask)    │         │
│  │  Port: 5173  │         │  Port: 5000  │         │
│  └──────────────┘         └───────┬──────┘         │
│                                   │                  │
│  ┌──────────────┐                 │                  │
│  │  University  │                 │                  │
│  │   Portal     │─────────────────┤                  │
│  │  (Flask)     │                 │                  │
│  │  Port: 3000  │                 │                  │
│  └──────────────┘                 │                  │
│                                   ▼                  │
│                          ┌──────────────┐           │
│                          │  PostgreSQL  │           │
│                          │   Database   │           │
│                          │  Port: 5432  │           │
│                          └──────────────┘           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Services
1. **Frontend (React)** - User interface for certificate upload
2. **Backend API (Flask)** - REST API with AI processing
3. **University Portal (Flask)** - Admin interface for student management
4. **PostgreSQL Database** - Data persistence

---

## 🛠️ Technology Stack

### Backend
- Flask 3.0.3
- SQLAlchemy 2.0.31
- PostgreSQL 16
- OpenAI GPT-4o-mini
- EasyOCR 1.7.0
- OpenCV 4.9.0+
- Gunicorn 21.2.0

### Frontend
- React 19.1.1
- Vite 7.1.2
- Axios 1.11.0
- React Router DOM 7.8.0

### Deployment
- Docker & Docker Compose
- Render (Production)
- Netlify (Frontend alternative)

---

## 📋 Prerequisites

- **Docker** and **Docker Compose** installed
- **OpenAI API Key** (required for AI features)
- **Git** for cloning the repository
- **Node.js 18+** (for local frontend development)
- **Python 3.9+** (for local backend development)

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd university-verifier
```

### 2. Environment Setup

Create `.env` file in project root:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# AI Configuration (REQUIRED)
OPENAI_API_KEY=sk-proj-your-key-here

# Database Configuration
POSTGRES_PASSWORD=your_secure_password_here
DB_URL=postgresql://postgres:your_password@localhost:5432/university_verifier

# Application Configuration
CORS_ORIGIN=http://localhost:3000,http://localhost:5173
UPLOAD_DIR=./uploads

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here

# Deployment
PORT=5000
HOST=0.0.0.0
```

### 3. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy and paste into `.env` file

---

## 🏃 Running Locally

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- University Portal: http://localhost:3000
- PostgreSQL: localhost:5432

### Option 2: Manual Setup

#### Backend
```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### University Portal
```bash
cd university-portal
pip install -r requirements.txt
python app.py
```

---

## ⚙️ Configuration

### Environment Variables

#### Backend Service
| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for AI extraction | - |
| `DATABASE_URL` | Yes | PostgreSQL connection string | - |
| `CORS_ORIGIN` | No | Allowed CORS origins | `*` |
| `UPLOAD_DIR` | No | File upload directory | `./uploads` |
| `MAX_FILE_SIZE` | No | Max upload size in bytes | `10485760` (10MB) |
| `JWT_SECRET` | Yes | Secret for JWT tokens | - |

#### Frontend Service
| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_URL` | Yes | Backend API URL |

#### University Portal
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `SECRET_KEY` | Yes | Flask secret key |

---

## 🚢 Deployment

### Deploy to Render (Recommended)

Render provides free hosting for all services.

#### Prerequisites
- GitHub account with repository
- Render account (free): https://render.com
- OpenAI API key

#### Steps

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Create Blueprint on Render**
- Go to https://dashboard.render.com/
- Click **"New"** → **"Blueprint"**
- Connect your GitHub repository
- Render will detect `render.yaml` automatically

3. **Configure Environment Variables**
- Find `university-verifier-backend` service
- Add `OPENAI_API_KEY` with your OpenAI key
- Other variables are auto-configured

4. **Deploy**
- Click **"Apply"** to start deployment
- Wait 15-20 minutes for all services to build
- You'll get URLs for each service

5. **Verify Deployment**
```bash
curl https://your-backend.onrender.com/api/v1/health

# Expected response:
{
  "status": "healthy",
  "ai_status": "configured",
  "version": "1.0.0"
}
```

### Cost Breakdown (Free Tier)

| Service | Cost | Limits |
|---------|------|--------|
| PostgreSQL | $0/month | 1GB storage, 90 days |
| Backend API | $0/month | Sleeps after 15min |
| Frontend | $0/month | 100GB bandwidth |
| Portal | $0/month | Sleeps after 15min |
| **Total** | **$0/month** | |

**Note**: Free tier services sleep after 15 minutes of inactivity and may take 30-60 seconds to wake up.

### Deploy Frontend to Netlify (Alternative)

1. **Build Frontend**
```bash
cd frontend
npm run build
```

2. **Deploy to Netlify**
- Go to https://app.netlify.com
- Drag and drop the `dist` folder
- Configure environment variable: `VITE_API_URL`

---

## 📡 API Documentation

### Base URL
- Local: `http://localhost:5000/api/v1`
- Production: `https://your-backend.onrender.com/api/v1`

### Endpoints

#### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "ai_status": "configured",
  "service": "University Certificate Verifier API",
  "version": "1.0.0"
}
```

#### Upload Certificate
```bash
POST /certificates/upload
Content-Type: multipart/form-data

Request Body:
file: <certificate-file>

Response:
{
  "id": 1,
  "file_type": "image",
  "summary": "AI-generated summary...",
  "tabular_data": {
    "student_name": "John Doe",
    "enrollment_number": "12345",
    "degree": "B.Tech",
    "branch": "Computer Science",
    ...
  },
  "verification": {
    "student_verified": true,
    "enrollment_verified": true,
    "confidence_score": 0.95
  }
}
```

#### List Certificates
```bash
GET /certificates?limit=20&offset=0

Response:
{
  "certificates": [...],
  "count": 10,
  "limit": 20,
  "offset": 0
}
```

#### Get Certificate Details
```bash
GET /certificates/{id}

Response:
{
  "id": 1,
  "status": "processed",
  "created_at": "2024-01-01T12:00:00",
  "summary": "...",
  "tabular_data": {...},
  "verification": {...}
}
```

#### Download Certificate
```bash
GET /certificates/{id}/download

Response: Binary file download
```

#### Export Certificate Data
```bash
GET /certificates/{id}/export

Response: JSON file download
```

### Authentication Endpoints

#### Register
```bash
POST /auth/register

Request:
{
  "username": "student123",
  "email": "student@example.com",
  "password": "password123",
  "user_type": "student",
  "student_name": "John Doe",
  "student_reg_no": "12345"
}

Response:
{
  "message": "User registered successfully",
  "token": "jwt-token",
  "user": {...}
}
```

#### Login
```bash
POST /auth/login

Request:
{
  "username": "student123",
  "password": "password123"
}

Response:
{
  "message": "Login successful",
  "token": "jwt-token",
  "user": {...}
}
```

---

## 🧪 Testing

### Test Certificate Upload

1. Access frontend at http://localhost:5173
2. Click "Upload Certificate"
3. Select or drag a certificate image/PDF
4. Click "Upload"
5. View AI-extracted data and verification results

### Test Backend Health
```bash
curl http://localhost:5000/api/v1/health
```

### Test University Portal
1. Access http://localhost:3000
2. Login with any alphanumeric username
3. Add student records
4. View uploaded certificates

---

## 🔧 Troubleshooting

### Common Issues

#### Backend Health Check Failing
**Problem**: Backend shows "Unhealthy"

**Solutions**:
1. Check OpenAI API key is set correctly
2. Verify DATABASE_URL is correct
3. Check logs: `docker-compose logs backend`
4. Ensure PostgreSQL is running

#### CORS Errors in Frontend
**Problem**: Browser shows CORS policy errors

**Solutions**:
1. Verify backend `CORS_ORIGIN` includes frontend URL
2. Check Flask-CORS is configured in `backend/app/main.py`
3. Restart backend service

#### AI Extraction Not Working
**Problem**: Certificate upload succeeds but extraction fails

**Solutions**:
1. Verify OpenAI API key is valid
2. Check API credits at https://platform.openai.com
3. Review backend logs for errors
4. Ensure model `gpt-4o-mini` is accessible

#### Database Connection Failed
**Problem**: Backend crashes on startup

**Solutions**:
1. Verify DATABASE_URL format:
   ```
   postgresql://user:password@host:port/database
   ```
2. Check PostgreSQL service is running
3. Ensure database name matches configuration

#### File Upload Size Limit
**Problem**: Upload fails for large files

**Solutions**:
1. Check `MAX_FILE_SIZE` environment variable
2. Default is 10MB (10485760 bytes)
3. Increase if needed (max 50MB recommended)

### Debug Mode

Enable debug logging in backend:

```python
# backend/app/main.py
app.run(debug=True)
```

View detailed logs:
```bash
docker-compose logs -f backend
```

---

## 📁 Project Structure

```
university-verifier/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   └── config.py          # Configuration
│   │   ├── db/
│   │   │   ├── models.py          # Database models
│   │   │   └── session.py         # DB session
│   │   ├── services/
│   │   │   ├── extract.py         # OpenAI extraction
│   │   │   ├── ocr.py             # OCR processing
│   │   │   └── images.py          # Image processing
│   │   └── main.py                # Flask app
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Upload.jsx         # Upload interface
│   │   │   ├── Records.jsx        # Certificate list
│   │   │   └── RecordDetail.jsx   # Detail view
│   │   ├── components/
│   │   │   └── Button.jsx         # Reusable button
│   │   ├── api/
│   │   │   └── axios.js           # API client
│   │   └── App.jsx                # Main component
│   ├── Dockerfile
│   └── package.json
├── university-portal/
│   ├── app.py                     # Flask portal
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml             # Local development
├── render.yaml                    # Render deployment
├── .env.example                   # Environment template
├── .gitignore                     # Git exclusions
└── README.md                      # This file
```

---

## 🔐 Security

### Best Practices
- ✅ Never commit `.env` files (already in `.gitignore`)
- ✅ Use environment variables for all secrets
- ✅ Rotate API keys periodically
- ✅ Use HTTPS in production (Render provides free SSL)
- ✅ Validate file uploads (type, size)
- ✅ Sanitize user inputs

### Environment Variables Security
- Store sensitive data in environment variables
- Use different values for development/production
- Never hardcode secrets in code

---

## 📊 Performance

### Optimization Tips
1. **Database Indexing** - Already implemented on key fields
2. **Image Preprocessing** - Optimizes images before OCR
3. **Caching** - Can add Redis for API response caching
4. **CDN** - Render serves static sites via CDN
5. **Compression** - Vite automatically compresses frontend assets

### Expected Performance
- Backend response: < 2s
- Frontend load: < 3s
- Certificate processing: < 10s (depends on OpenAI API)
- Database queries: < 100ms

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

- **Documentation**: This README file
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Render Support**: https://render.com/docs
- **OpenAI Support**: https://help.openai.com

---

## ✅ Deployment Checklist

Before deploying to production:

- [ ] All code committed to GitHub
- [ ] `.env` file NOT committed (in `.gitignore`)
- [ ] OpenAI API key ready
- [ ] Render account created
- [ ] `render.yaml` present in repository
- [ ] Environment variables configured
- [ ] Tested locally with Docker
- [ ] Database migrations ready (auto-created on startup)

After deployment:

- [ ] Backend health check returns `{"status": "healthy"}`
- [ ] Frontend loads without errors
- [ ] Certificate upload works end-to-end
- [ ] University portal accessible
- [ ] AI extraction functional

---

## 🎉 Quick Start Summary

```bash
# 1. Clone and setup
git clone <repo-url>
cd university-verifier
cp .env.example .env
# Edit .env with your OpenAI API key

# 2. Run with Docker
docker-compose up -d

# 3. Access services
# Frontend: http://localhost:5173
# Backend: http://localhost:5000
# Portal: http://localhost:3000

# 4. Test
curl http://localhost:5000/api/v1/health

# 5. Deploy to Render
git push origin main
# Then follow Render Blueprint steps above
```

---

**Status**: ✅ Production Ready  
**Deployment Time**: 15-20 minutes  
**Cost**: $0/month (free tier)

**Built with ❤️ using AI technology**
