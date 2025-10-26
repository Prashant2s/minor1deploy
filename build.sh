#!/bin/bash
# Build script for Render deployment

set -e

echo "🚀 Starting build process..."

# Backend setup
echo "📦 Setting up backend..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Frontend setup
echo "🎨 Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build completed successfully!"
