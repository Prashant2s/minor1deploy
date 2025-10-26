#!/bin/bash

# AI-Powered University Certificate Verifier - Deployment Script
# This script helps set up the project for deployment

echo "🚀 AI-Powered University Certificate Verifier - Deployment Setup"
echo "================================================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  IMPORTANT: Please edit .env file and add your OpenAI API key!"
    echo "   Without the API key, this AI-powered application will not function."
    echo ""
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Check if .env has OpenAI API key
if grep -q "your_openai_api_key_here" .env; then
    echo "⚠️  WARNING: Please update your OpenAI API key in .env file before running!"
    echo "   The application requires an OpenAI API key to function."
    echo ""
fi

echo "🔧 Building and starting the application..."
echo "   This will:"
echo "   - Build the backend with AI processing capabilities"
echo "   - Build the frontend for Netlify deployment"
echo "   - Start PostgreSQL database"
echo "   - Start the AI-powered certificate processing service"
echo ""

# Build and start the application
docker-compose --env-file .env up --build

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Frontend: http://localhost:5173"
echo "   2. Backend API: http://localhost:5000/health"
echo "   3. For Netlify deployment:"
echo "      - Update netlify.toml with your backend URL"
echo "      - Set VITE_API_URL environment variable in Netlify"
echo "      - Deploy the frontend/dist folder"
echo ""
echo "🤖 This is an AI-powered project that requires OpenAI API key for all functionality!"
