# AI-Powered University Certificate Verifier

An advanced AI-powered certificate verification system that extracts and summarizes academic certificates using OpenAI API, advanced OCR, and PostgreSQL database. This is a college project that demonstrates cutting-edge AI integration for document processing and verification.

## 🚀 AI Features

- **AI-Powered Extraction**: Uses OpenAI GPT-4o-mini for intelligent field extraction (API key REQUIRED)
- **Advanced OCR Processing**: EasyOCR with enhanced image preprocessing for optimal text recognition from certificates
- **Tabular Data Extraction**: AI focuses exclusively on structured tabular data from academic certificates - NO raw text output
- **Smart Field Recognition**: Extracts 16+ fields including names, enrollment numbers, grades, CGPA, SGPA, subjects, and credits
- **AI-Generated Summaries**: Creates concise, professional summaries of certificate information for easy display
- **Subject-wise Performance**: Extracts detailed subject codes, names, grades, and credits in structured tabular format
- **Multi-Format Support**: Handles PDF, JPG, JPEG, PNG, TIFF, BMP, WEBP files with intelligent preprocessing
- **Strict API Key Requirement**: This AI project REQUIRES OpenAI API key - no fallback methods provided
- **University Verification**: Compares AI-extracted data with university database
- **Docker Deployment**: Ready for production deployment
- **Netlify Ready**: Frontend optimized for Netlify deployment

## 🎯 Key AI Capabilities

- **Structured Data Extraction**: AI identifies and extracts tabular information from certificates
- **Academic Performance Analysis**: Extracts grades, CGPA, SGPA, and semester-wise performance
- **Smart Text Processing**: Handles complex certificate layouts and formats
- **Confidence Scoring**: Provides confidence levels for extracted information
- **Professional Summarization**: Generates clean, display-ready summaries

## 🏗️ Project Structure

```
university-verifier/
├── backend/                 # Flask API with AI processing
│   ├── app/
│   │   ├── api/            # API routes and endpoints
│   │   │   └── routes.py   # Certificate upload and retrieval endpoints
│   │   ├── core/           # Configuration and settings
│   │   │   └── config.py   # Environment variables and app configuration
│   │   ├── db/             # Database models and session
│   │   │   ├── models.py   # SQLAlchemy models for certificates
│   │   │   └── session.py  # Database session management
│   │   ├── services/       # AI extraction and OCR services
│   │   │   ├── extract.py  # OpenAI API integration for field extraction
│   │   │   ├── images.py   # Image processing and optimization
│   │   │   └── ocr.py      # EasyOCR text recognition service
│   │   └── main.py         # Flask application entry point
│   ├── requirements.txt    # Python dependencies
│   ├── run_local.py        # Local development runner
│   └── wipe_certs.py       # Database cleanup utility
├── frontend/               # React application
│   ├── src/
│   │   ├── pages/          # React components and pages
│   │   │   ├── Upload.jsx  # Certificate upload interface
│   │   │   ├── Records.jsx # List of processed certificates
│   │   │   └── RecordDetail.jsx # Detailed certificate view
│   │   ├── api/            # API client configuration
│   │   │   └── axios.js    # HTTP client setup
│   │   ├── App.jsx         # Main application component with routing
│   │   ├── App.css         # Application styles
│   │   └── main.jsx        # React application entry point
│   ├── public/             # Static assets
│   ├── dist/               # Built frontend files for production
│   ├── package.json        # Node.js dependencies and scripts
│   ├── vite.config.js      # Vite build configuration
│   └── eslint.config.js    # ESLint configuration
├── docker/                 # Docker configuration files
│   ├── backend.Dockerfile  # Backend container configuration
│   └── frontend.Dockerfile # Frontend container configuration
├── docker-compose.yml      # Multi-container setup
├── deploy.bat              # Windows deployment script
├── deploy.sh               # Linux/Mac deployment script
├── netlify.toml            # Netlify configuration
├── Procfile                # Heroku deployment configuration
├── runtime.txt             # Python runtime version for Heroku
├── env.example             # Environment variables template
├── university.db           # SQLite database (local development)
└── uploads/                # Directory for uploaded certificate files
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API Key (required for AI functionality - this is an AI-powered project)
- PostgreSQL database (included in Docker setup)
- Node.js 18+ (for local frontend development)
- Python 3.9+ (for local backend development)

### Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd university-verifier
   ```

2. **Copy environment file**:

   ```bash
   cp env.example .env
   ```

3. **Edit `.env` and set your OpenAI API key**:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   POSTGRES_PASSWORD=your_secure_password
   ```

4. **Build and run with Docker**:

   ```bash
   # Windows
   deploy.bat

   # Linux/Mac
   ./deploy.sh

   # Or manually
   docker-compose --env-file .env up --build
   ```

5. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:5000/health

## 📊 AI Extraction Fields

The AI-powered system extracts the following fields from certificates in tabular format:

- **Student Name**: Full name of the student
- **Enrollment Number**: Official enrollment number
- **Degree Program**: B.Tech, B.E., M.Tech, B.Sc, etc.
- **Branch/Department**: Computer Science & Engineering, Electronics, etc.
- **University Name**: Complete university/institution name
- **Graduation Date**: Date of graduation/completion (DD/MM/YYYY)
- **Date of Birth**: Student's date of birth if available
- **Academic Performance**: CGPA/SGPA numerical values
- **Certificate Type**: Degree Certificate, Transcript, Semester Result, etc.
- **Semester Information**: Semester 1, Semester 2, etc.
- **Academic Year**: Academic year (2023-24, 2024, etc.)
- **Total Credits**: Total credit points for the semester/course
- **Earned Credits**: Credits earned by the student
- **Subject-wise Performance**: Array of subjects with codes, names, grades, and credits

## 🔧 Technology Stack

### Backend (AI-Powered)

- **Flask 3.0.3** with SQLAlchemy 2.0.31 for API development
- **PostgreSQL 16** database for data storage
- **OpenAI GPT-4o-mini** for AI-powered field extraction and summarization
- **EasyOCR 1.7.0** for advanced text recognition
- **OpenCV 4.9.0+** for enhanced image preprocessing
- **PyMuPDF 1.24.0** for PDF processing
- **Pillow 10.4.0** for image manipulation
- **NumPy 1.26.0+** for numerical processing
- **PyTorch 2.2.0+** for AI model support
- **Gunicorn 21.2.0** for production WSGI server

### Frontend (Modern React)

- **React 19.1.1** with Vite 7.1.2 for fast development
- **Material-UI 7.3.1** for modern UI components
- **React Router DOM 7.8.0** for navigation
- **Axios 1.11.0** for API communication
- **Emotion** for CSS-in-JS styling
- **ESLint 9.33.0** for code quality
- **Responsive Design** for all devices
- **AI-Focused Interface** highlighting AI capabilities
- File upload with drag-and-drop support

## 📡 API Endpoints

### Certificate Management

- `POST /api/v1/certificates/upload` - Upload certificate file
- `GET /api/v1/certificates` - List all certificates
- `GET /api/v1/certificates/{id}` - Get certificate details
- `GET /api/v1/certificates/{id}/image` - Get certificate image

### System

- `GET /health` - Health check endpoint

### API Request/Response Examples

**Upload Certificate**:

```bash
POST /api/v1/certificates/upload
Content-Type: multipart/form-data

# Form data with 'file' field containing the certificate image/PDF
```

**Get Certificate Details**:

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
  "confidence_score": 0.95
}
```

## 🌐 Deployment

### Frontend Deployment (Netlify)

1. **Connect repository to Netlify**
2. **Update configuration**:
   - Edit `netlify.toml` and replace `your-backend-url.herokuapp.com` with your actual backend URL
   - Set `VITE_API_URL` environment variable in Netlify dashboard
3. **Deploy**: Netlify will automatically build and deploy from the `frontend/dist` folder

**Netlify Configuration**:

```toml
[build]
  command = "cd frontend && npm install && npm run build"
  publish = "frontend/dist"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/api/*"
  to = "https://your-backend-url.herokuapp.com/api/:splat"
  status = 200
```

### Backend Deployment Options

#### Option 1: Heroku

1. **Install Heroku CLI**
2. **Create Heroku App**:
   ```bash
   heroku create your-app-name
   ```
3. **Add PostgreSQL Addon**:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
4. **Set Environment Variables**:
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key
   heroku config:set POSTGRES_PASSWORD=your_secure_password
   ```
5. **Deploy**:
   ```bash
   git push heroku main
   ```

#### Option 2: Railway

1. Go to [Railway](https://railway.app)
2. Connect your GitHub repository
3. Select the backend folder
4. Set environment variables in Railway dashboard
5. Deploy automatically

#### Option 3: Render

1. Go to [Render](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `cd backend && pip install -r requirements.txt`
5. Set start command: `cd backend && gunicorn app.main:create_app`
6. Add PostgreSQL database
7. Set environment variables

#### Option 4: DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create a new app from GitHub
3. Select backend folder
4. Configure build and run commands
5. Add PostgreSQL database
6. Set environment variables

### Environment Variables for Production

Set these in your deployment platform:

```bash
OPENAI_API_KEY=your_openai_api_key_here
POSTGRES_PASSWORD=your_secure_password
DB_URL=postgresql://user:password@host:port/database
CORS_ORIGIN=https://your-frontend-domain.netlify.app
MAX_FILE_SIZE=10485760
LOG_LEVEL=INFO
```

## 📋 Environment Variables

| Variable            | Description                      | Required | Default               |
| ------------------- | -------------------------------- | -------- | --------------------- |
| `OPENAI_API_KEY`    | OpenAI API key for AI extraction | Yes      | -                     |
| `POSTGRES_PASSWORD` | Database password                | Yes      | -                     |
| `DB_URL`            | PostgreSQL connection string     | Auto     | -                     |
| `CORS_ORIGIN`       | CORS allowed origins             | No       | http://localhost:5173 |
| `MAX_FILE_SIZE`     | Maximum file upload size (bytes) | No       | 10485760              |
| `LOG_LEVEL`         | Logging level                    | No       | INFO                  |
| `UPLOAD_DIR`        | Directory for uploaded files     | No       | /data/uploads         |

## 🎓 College Project Features

- **Advanced AI Integration**: Demonstrates cutting-edge AI integration with OpenAI API
- **Modern Web Development**: Shows best practices with React, Flask, and PostgreSQL
- **Comprehensive Deployment**: Multiple deployment options for different platforms
- **Professional UI/UX**: Material-UI design with responsive layout
- **Database Optimization**: Efficient data storage and retrieval
- **Production Ready**: Docker containerization and CI/CD setup
- **Documentation**: Comprehensive setup and deployment guides
- **Scalable Architecture**: Microservices-ready with separate frontend/backend

## 🔍 Supported File Formats

- **PDF**: Academic transcripts and certificates (PyMuPDF processing)
- **Images**: JPG, JPEG, PNG, TIFF, BMP, WEBP (Pillow + OpenCV)
- **Maximum file size**: 10MB (configurable via MAX_FILE_SIZE)
- **OCR Support**: EasyOCR with 80+ language support

## 📊 Tabular Data Format

The system presents extracted information in a clean, structured table format:

- **Field**: The extracted field name
- **Value**: The extracted value
- **Confidence**: AI confidence score for the extraction (0.0 - 1.0)

**Example Output**:

```
┌─────────────────────────┬──────────────────────┬────────────┐
│ Field                   │ Value                │ Confidence │
├─────────────────────────┼──────────────────────┼────────────┤
│ Student Name            │ John Doe             │ 0.98       │
│ Enrollment Number       │ 12345678             │ 0.95       │
│ Degree Program          │ B.Tech               │ 0.92       │
│ CGPA                    │ 8.5                  │ 0.89       │
└─────────────────────────┴──────────────────────┴────────────┘
```

## 🛠️ Development

### Local Development Setup

1. **Backend Development**:

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python run_local.py
   ```

2. **Frontend Development**:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Database Management**:
   - The application automatically creates required tables on first run
   - Use `backend/wipe_certs.py` to clear all certificate data
   - Database file: `university.db` (SQLite for local development)

### Development Scripts

**Docker Development (IMPORTANT - Always refresh after changes)**:

```bash
# Windows - Full refresh (recommended for major changes)
refresh-docker.bat

# Windows - Quick refresh (faster, for minor changes)
quick-refresh.bat

# PowerShell
.\refresh-docker.ps1

# Manual commands
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

**Frontend**:

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

**Backend**:

```bash
python run_local.py     # Start Flask development server
python wipe_certs.py    # Clear all certificate data
```

### Code Structure

**Backend Services**:

- `services/extract.py`: OpenAI API integration for field extraction
- `services/ocr.py`: EasyOCR text recognition
- `services/images.py`: Image processing and optimization
- `api/routes.py`: REST API endpoints
- `db/models.py`: SQLAlchemy database models

**Frontend Components**:

- `pages/Upload.jsx`: Certificate upload interface
- `pages/Records.jsx`: List of processed certificates
- `pages/RecordDetail.jsx`: Detailed certificate view
- `api/axios.js`: HTTP client configuration

## ⚠️ Important Notes

1. **API Key Required**: This is an AI-powered project that requires OpenAI API key for all functionality
2. **No Fallback Methods**: The system is designed to be strictly AI-dependent
3. **Tabular Focus**: All data is presented in structured tabular format, not raw text
4. **Production Ready**: Includes Docker setup, database optimization, and deployment configurations
5. **Cost Consideration**: OpenAI API usage incurs costs based on token consumption

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**:

   - Make sure `CORS_ORIGIN` is set to your frontend URL
   - Check that the frontend URL matches exactly (including protocol)

2. **API Key Missing**:

   - Ensure `OPENAI_API_KEY` is set correctly in your environment
   - Verify the API key has sufficient credits

3. **Database Connection**:

   - Check if PostgreSQL is running and accessible
   - Verify connection string format

4. **File Upload Issues**:

   - Verify `MAX_FILE_SIZE` is appropriate
   - Check file format is supported
   - Ensure upload directory has write permissions

5. **Docker Issues**:

   - Ensure Docker and Docker Compose are properly installed
   - Check if ports 5000 and 5173 are available
   - Verify .env file exists and has correct values

6. **AI Processing Errors**:
   - Check OpenAI API key validity
   - Verify sufficient API credits
   - Check image quality and format

### Logs and Debugging

- **Local Development**: Check console output for both frontend and backend
- **Docker**:
  ```bash
  docker-compose logs backend
  docker-compose logs frontend
  docker-compose logs db
  ```
- **Production**: Check logs in your deployment platform dashboard

### Performance Issues

- **Slow AI Processing**: Consider image optimization before OCR
- **Large File Uploads**: Implement progress indicators
- **Database Queries**: Monitor query performance and add indexes if needed

## 🔒 Security Considerations

1. **API Keys**:

   - Never commit API keys to version control
   - Use environment variables for all sensitive data
   - Rotate API keys regularly

2. **CORS**:

   - Set appropriate CORS origins for production
   - Avoid using wildcard (\*) in production

3. **File Uploads**:

   - Implement file size limits and type validation
   - Scan uploaded files for malware
   - Store files outside web root

4. **Database**:

   - Use strong passwords and secure connections
   - Enable SSL/TLS for database connections
   - Regular security updates

5. **Environment Variables**:
   - Use secure environment variable management
   - Never log sensitive environment variables

## 📈 Performance Optimization

1. **Image Processing**:

   - Consider using CDN for uploaded images
   - Implement image compression and resizing
   - Use WebP format for better compression

2. **Database**:

   - Use connection pooling for high traffic
   - Add appropriate indexes for frequently queried fields
   - Consider read replicas for scaling

3. **Caching**:

   - Implement Redis for frequently accessed data
   - Cache AI extraction results
   - Use browser caching for static assets

4. **Monitoring**:

   - Set up application monitoring and alerts
   - Monitor API response times
   - Track OpenAI API usage and costs

5. **AI Processing**:
   - Optimize OpenAI API calls for cost efficiency
   - Implement request queuing for high volume
   - Cache similar extraction results

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**:
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed
4. **Test with Docker**: `docker-compose up --build`
5. **Commit your changes**: `git commit -m 'Add feature'`
6. **Push to the branch**: `git push origin feature-name`
7. **Submit a pull request**

### Development Guidelines

- Use meaningful commit messages
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Add comments for complex AI processing logic
- Test all changes with Docker setup

## 📞 Support

For issues or questions:

1. **Check this README** for detailed setup instructions
2. **Verify your OpenAI API key** is correctly configured
3. **Ensure Docker and Docker Compose** are properly installed
4. **Check the deployment logs** for any errors
5. **Review the troubleshooting section** above
6. **Check GitHub Issues** for similar problems

### Getting Help

- **Documentation**: This README contains comprehensive setup and deployment guides
- **Docker Logs**: Use `docker-compose logs` to debug issues
- **API Testing**: Use tools like Postman to test API endpoints
- **Browser DevTools**: Check network requests and console errors

## 📄 License

This project is for educational purposes and demonstrates modern AI integration in web applications.

## 🎯 Project Goals

This AI-powered university certificate verifier serves as a comprehensive demonstration of:

- **Modern AI Integration**: Showcasing OpenAI API capabilities
- **Full-Stack Development**: React frontend with Flask backend
- **Database Design**: Efficient data storage and retrieval
- **Deployment Strategies**: Multiple platform deployment options
- **Production Readiness**: Docker, monitoring, and security considerations
- **Documentation**: Comprehensive guides for setup and deployment

---

**This is an AI-powered college project showcasing cutting-edge AI integration with OpenAI API for intelligent document processing and verification.**
