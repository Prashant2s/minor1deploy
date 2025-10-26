# Simple Setup Guide - Certificate Verifier with University Portal

## Quick Overview

This project has 3 main components:
1. **Backend** (Port 5000) - Flask API with AI-powered certificate extraction
2. **Frontend** (Port 5173) - React app for certificate upload
3. **University Portal** (Port 3000) - University database for verification

The Backend automatically verifies certificates against the University Portal database.

## Prerequisites

- Docker and Docker Compose
- OpenAI API Key (required for AI features)
- Git

## Quick Start

### 1. Setup Environment

Copy the environment file and add your API key:

```bash
cp env.example .env
```

Edit `.env` and add:
```
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_PASSWORD=your_secure_password
```

### 2. Start with Docker

```bash
# Windows
docker-compose up --build

# Or use the provided script
.\deploy.bat
```

This will start all three services:
- Backend: http://localhost:5000
- Frontend: http://localhost:5173
- University Portal: http://localhost:3000

### 3. Access the Application

1. Open http://localhost:5173 in your browser
2. Upload a certificate (PDF, JPG, PNG)
3. The system will:
   - Extract data using AI
   - Verify against university database
   - Display results with verification status

### 4. Test University Portal

Open http://localhost:3000 to:
- View all certificates in university database
- Search by enrollment number
- Upload new certificates to university database
- Use API for integration

## How Verification Works

When you upload a certificate:

1. **AI Extraction**: Backend extracts student name, enrollment number, CGPA, etc.
2. **University Verification**: Backend sends extracted data to University Portal
3. **Database Check**: University Portal checks against `university-portal/database/certificates.json`
4. **Result**: Frontend shows verification status (✅ Verified or ❌ Not Found)

## Sample Data

The University Portal comes with 5 sample certificates:
- Arjun Kumar Sharma (19BTCSE001) - CSE
- Priya Singh (19BTECE002) - ECE
- Rahul Patel (20BTME003) - ME
- Sneha Gupta (21BTIT004) - IT
- Amit Verma (18BTCSE005) - CSE

## Adding Certificates to University Database

### Option 1: Using the Portal UI
1. Go to http://localhost:3000
2. Click "Upload Certificate"
3. Fill the form and submit

### Option 2: Using the API
```bash
curl -X POST http://localhost:3000/api/certificates \
  -H "Content-Type: application/json" \
  -d '{
    "student_name": "John Doe",
    "enrollment_number": "22BTCSE001",
    "branch": "Computer Science Engineering",
    "cgpa": 8.5,
    "academic_year": "2022-2026",
    "status": "Pass"
  }'
```

## Project Structure

```
university-verifier/
├── backend/                    # Flask API
│   ├── app/
│   │   ├── services/
│   │   │   ├── extract.py     # AI extraction & verification
│   │   │   ├── ocr.py         # Text recognition
│   │   │   └── images.py      # Image processing
│   │   └── api/routes.py      # API endpoints
│   └── requirements.txt
├── frontend/                   # React app
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Upload.jsx     # Upload page
│   │   │   └── Records.jsx    # View records
│   │   └── App.jsx
│   └── package.json
├── university-portal/          # University database
│   ├── backend/
│   │   └── app.py             # Flask API
│   ├── database/
│   │   └── certificates.json  # Certificate database
│   └── frontend/
│       └── index.html         # Portal UI
└── docker-compose.yml         # Docker setup
```

## API Endpoints

### Backend (Port 5000)
- `POST /api/v1/certificates/upload` - Upload & analyze certificate
- `GET /api/v1/certificates` - List all uploaded certificates
- `GET /api/v1/certificates/{id}` - Get certificate details

### University Portal (Port 3000)
- `GET /api/certificates` - List all university certificates
- `POST /api/certificates` - Add new certificate
- `GET /api/certificates/{enrollment}` - Get by enrollment
- `POST /api/verify` - Verify certificate data
- `GET /api/stats` - University statistics

## Troubleshooting

### Backend won't start
- Check if OpenAI API key is set in `.env`
- Verify Docker is running
- Check port 5000 is not in use

### University Portal connection fails
- Make sure all containers are running: `docker-compose ps`
- Check logs: `docker-compose logs university-portal`

### Frontend can't connect to backend
- Verify backend is running at http://localhost:5000/health
- Check CORS settings in backend

### Docker refresh (after making changes)
```bash
# Windows
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=sk-...                    # Required for AI features
POSTGRES_PASSWORD=password               # Database password
UNIVERSITY_PORTAL_URL=http://university-portal:3000  # Auto-set in Docker
```

### Frontend
```
VITE_API_URL=http://localhost:5000/api/v1  # Backend API URL
```

## Deployment to Netlify (Frontend Only)

After testing locally:

1. Push code to GitHub
2. Connect repository to Netlify
3. Update `netlify.toml`:
   ```toml
   [[redirects]]
     from = "/api/*"
     to = "https://your-backend-url.com/api/:splat"
     status = 200
   ```
4. Set environment variable in Netlify:
   ```
   VITE_API_URL=https://your-backend-url.com/api/v1
   ```

For backend deployment, consider:
- Heroku
- Railway
- Render
- DigitalOcean

## Features

✅ AI-powered certificate extraction (OpenAI GPT-4o-mini)
✅ University database verification
✅ OCR text recognition
✅ PDF and image support
✅ Subject-wise grade extraction
✅ Professional summaries
✅ Confidence scoring
✅ Docker deployment ready

## Notes

- The summarizer functionality remains **unchanged** - it still uses OpenAI to generate summaries
- All AI features require a valid OpenAI API key
- University Portal uses a simple JSON file for storage (production should use PostgreSQL)
- Frontend and Backend use separate databases (Backend: PostgreSQL, Portal: JSON)
