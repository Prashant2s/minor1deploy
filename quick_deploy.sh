#!/bin/bash

# Quick Deployment Script for AI Certificate Verifier
# This script helps you deploy the application quickly

echo "🚀 AI Certificate Verifier - Quick Deployment"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "netlify.toml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📋 Pre-deployment checks..."

# Test backend
echo "Testing backend..."
cd backend
if python test_deployment.py; then
    echo "✅ Backend tests passed"
else
    echo "❌ Backend tests failed. Please fix issues before deploying."
    exit 1
fi
cd ..

# Test frontend build
echo "Testing frontend build..."
cd frontend
if npm run build; then
    echo "✅ Frontend build successful"
else
    echo "❌ Frontend build failed. Please fix issues before deploying."
    exit 1
fi
cd ..

echo ""
echo "🎯 Deployment Options:"
echo "1. Railway (Recommended for backend)"
echo "2. Render (Alternative for backend)"
echo "3. Heroku (Traditional option)"
echo "4. Netlify (Frontend only)"
echo ""

read -p "Choose deployment option (1-4): " choice

case $choice in
    1)
        echo "🚂 Railway Deployment"
        echo "1. Go to https://railway.app"
        echo "2. Connect your GitHub repository"
        echo "3. Select the 'backend' folder"
        echo "4. Set environment variables:"
        echo "   - OPENAI_API_KEY=your_openai_api_key"
        echo "   - POSTGRES_PASSWORD=your_secure_password"
        echo "   - CORS_ORIGIN=https://your-frontend-domain.netlify.app"
        echo "5. Deploy automatically"
        ;;
    2)
        echo "🎨 Render Deployment"
        echo "1. Go to https://render.com"
        echo "2. Create a new Web Service"
        echo "3. Connect your GitHub repository"
        echo "4. Set build command: cd backend && pip install -r requirements.txt"
        echo "5. Set start command: cd backend && gunicorn app.main:app"
        echo "6. Add PostgreSQL database"
        echo "7. Set environment variables"
        ;;
    3)
        echo "🟣 Heroku Deployment"
        echo "1. Install Heroku CLI"
        echo "2. Run: heroku create your-app-name"
        echo "3. Run: heroku addons:create heroku-postgresql:mini"
        echo "4. Set environment variables:"
        echo "   heroku config:set OPENAI_API_KEY=your_openai_api_key"
        echo "   heroku config:set POSTGRES_PASSWORD=your_secure_password"
        echo "5. Run: git push heroku main"
        ;;
    4)
        echo "🌐 Netlify Deployment (Frontend)"
        echo "1. Go to https://netlify.com"
        echo "2. Connect your GitHub repository"
        echo "3. Update netlify.toml with your backend URL"
        echo "4. Set VITE_API_URL environment variable"
        echo "5. Deploy automatically"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "📚 For detailed instructions, see:"
echo "- DEPLOYMENT_GUIDE.md"
echo "- DEPLOYMENT_CHECKLIST.md"
echo ""
echo "🔧 Environment Variables Needed:"
echo "Backend:"
echo "  OPENAI_API_KEY=your_openai_api_key_here"
echo "  POSTGRES_PASSWORD=your_secure_password"
echo "  CORS_ORIGIN=https://your-frontend-domain.netlify.app"
echo ""
echo "Frontend (Netlify):"
echo "  VITE_API_URL=https://your-backend-url.railway.app/api/v1"
echo ""
echo "🎉 Happy deploying!"
