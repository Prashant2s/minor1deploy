# Test Docker Deployment Script
# This script tests all three services after Docker deployment

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing University Verifier Deployment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[1/7] Checking if Docker is running..." -ForegroundColor Yellow
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Docker is running" -ForegroundColor Green
Write-Host ""

# Check if containers are running
Write-Host "[2/7] Checking running containers..." -ForegroundColor Yellow
$containers = docker-compose ps --services --filter "status=running"
$expectedServices = @("db", "backend", "frontend", "university-portal")
$runningServices = $containers -split "`n" | Where-Object { $_ -ne "" }

foreach ($service in $expectedServices) {
    if ($runningServices -contains $service) {
        Write-Host "✓ $service is running" -ForegroundColor Green
    } else {
        Write-Host "✗ $service is NOT running" -ForegroundColor Red
    }
}
Write-Host ""

# Test University Portal
Write-Host "[3/7] Testing University Portal (http://localhost:3000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ University Portal is responding" -ForegroundColor Green
        $content = $response.Content | ConvertFrom-Json
        Write-Host "  Service: $($content.service)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ University Portal is not responding: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Backend
Write-Host "[4/7] Testing Backend API (http://localhost:5000)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend is responding" -ForegroundColor Green
        $content = $response.Content | ConvertFrom-Json
        Write-Host "  Status: $($content.status)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Backend is not responding: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Frontend
Write-Host "[5/7] Testing Frontend (http://localhost:5173)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Frontend is responding" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Frontend is not responding: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test University Portal API
Write-Host "[6/7] Testing University Portal API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000/api/certificates" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        $content = $response.Content | ConvertFrom-Json
        Write-Host "✓ University Portal API is working" -ForegroundColor Green
        Write-Host "  Total certificates in database: $($content.total)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ University Portal API is not working: $($_.Exception.Message)" -ForegroundColor Red
}
Write-Host ""

# Test Backend to University Portal connection
Write-Host "[7/7] Testing Backend to University Portal connection..." -ForegroundColor Yellow
Write-Host "  This test requires uploading a certificate to verify integration." -ForegroundColor Gray
Write-Host "  To test manually:" -ForegroundColor Gray
Write-Host "  1. Go to http://localhost:5173" -ForegroundColor Gray
Write-Host "  2. Upload a certificate" -ForegroundColor Gray
Write-Host "  3. Check if verification status shows" -ForegroundColor Gray
Write-Host ""

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access points:" -ForegroundColor Yellow
Write-Host "  Frontend:         http://localhost:5173" -ForegroundColor White
Write-Host "  Backend API:      http://localhost:5000/health" -ForegroundColor White
Write-Host "  University Portal: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open http://localhost:5173 in your browser" -ForegroundColor White
Write-Host "  2. Upload a test certificate" -ForegroundColor White
Write-Host "  3. Verify it shows verification status" -ForegroundColor White
Write-Host "  4. Check http://localhost:3000 to view university database" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  docker-compose logs backend" -ForegroundColor White
Write-Host "  docker-compose logs frontend" -ForegroundColor White
Write-Host "  docker-compose logs university-portal" -ForegroundColor White
Write-Host ""
