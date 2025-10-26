@echo off
REM Quick Deployment Script for AI Certificate Verifier (Windows)
REM This script helps you deploy the application quickly

echo 🚀 AI Certificate Verifier - Quick Deployment
echo ==============================================

REM Check if we're in the right directory
if not exist "netlify.toml" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

echo 📋 Pre-deployment checks...

REM Test backend
echo Testing backend...
cd backend
python test_deployment.py
if %errorlevel% neq 0 (
    echo ❌ Backend tests failed. Please fix issues before deploying.
    pause
    exit /b 1
)
echo ✅ Backend tests passed
cd ..

REM Test frontend build
echo Testing frontend build...
cd frontend
call npm run build
if %errorlevel% neq 0 (
    echo ❌ Frontend build failed. Please fix issues before deploying.
    pause
    exit /b 1
)
echo ✅ Frontend build successful
cd ..

echo.
echo 🎯 Deployment Options:
echo 1. Railway (Recommended for backend)
echo 2. Render (Alternative for backend)
echo 3. Heroku (Traditional option)
echo 4. Netlify (Frontend only)
echo.

set /p choice="Choose deployment option (1-4): "

if "%choice%"=="1" (
    echo 🚂 Railway Deployment
    echo 1. Go to https://railway.app
    echo 2. Connect your GitHub repository
    echo 3. Select the 'backend' folder
    echo 4. Set environment variables:
    echo    - OPENAI_API_KEY=your_openai_api_key
    echo    - POSTGRES_PASSWORD=your_secure_password
    echo    - CORS_ORIGIN=https://your-frontend-domain.netlify.app
    echo 5. Deploy automatically
) else if "%choice%"=="2" (
    echo 🎨 Render Deployment
    echo 1. Go to https://render.com
    echo 2. Create a new Web Service
    echo 3. Connect your GitHub repository
    echo 4. Set build command: cd backend ^&^& pip install -r requirements.txt
    echo 5. Set start command: cd backend ^&^& gunicorn app.main:app
    echo 6. Add PostgreSQL database
    echo 7. Set environment variables
) else if "%choice%"=="3" (
    echo 🟣 Heroku Deployment
    echo 1. Install Heroku CLI
    echo 2. Run: heroku create your-app-name
    echo 3. Run: heroku addons:create heroku-postgresql:mini
    echo 4. Set environment variables:
    echo    heroku config:set OPENAI_API_KEY=your_openai_api_key
    echo    heroku config:set POSTGRES_PASSWORD=your_secure_password
    echo 5. Run: git push heroku main
) else if "%choice%"=="4" (
    echo 🌐 Netlify Deployment (Frontend)
    echo 1. Go to https://netlify.com
    echo 2. Connect your GitHub repository
    echo 3. Update netlify.toml with your backend URL
    echo 4. Set VITE_API_URL environment variable
    echo 5. Deploy automatically
) else (
    echo ❌ Invalid option
    pause
    exit /b 1
)

echo.
echo 📚 For detailed instructions, see:
echo - DEPLOYMENT_GUIDE.md
echo - DEPLOYMENT_CHECKLIST.md
echo.
echo 🔧 Environment Variables Needed:
echo Backend:
echo   OPENAI_API_KEY=your_openai_api_key_here
echo   POSTGRES_PASSWORD=your_secure_password
echo   CORS_ORIGIN=https://your-frontend-domain.netlify.app
echo.
echo Frontend (Netlify):
echo   VITE_API_URL=https://your-backend-url.railway.app/api/v1
echo.
echo 🎉 Happy deploying!
pause
