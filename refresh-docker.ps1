#!/usr/bin/env pwsh

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Docker Refresh Script for PowerShell" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/4] Stopping containers..." -ForegroundColor Yellow
docker-compose down

Write-Host ""
Write-Host "[2/4] Rebuilding images with latest changes..." -ForegroundColor Yellow
docker-compose build --no-cache

Write-Host ""
Write-Host "[3/4] Starting containers in detached mode..." -ForegroundColor Yellow
docker-compose up -d

Write-Host ""
Write-Host "[4/4] Checking container status..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   Docker refresh complete!" -ForegroundColor Green
Write-Host "   Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "   Backend:  http://localhost:5000" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to continue"