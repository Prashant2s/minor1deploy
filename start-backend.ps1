# Start Main Backend Server on port 5000
Write-Host "🚀 Starting Certificate Verifier Backend..." -ForegroundColor Cyan
Write-Host ""

Set-Location -Path "backend"

# Check if port 5000 is already in use
$port = 5000
$listener = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue

if ($listener) {
    Write-Host "⚠️  Port $port is already in use!" -ForegroundColor Yellow
    Write-Host "Backend may already be running." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To check: curl http://localhost:5000/health" -ForegroundColor Gray
} else {
    Write-Host "Starting Flask server on http://localhost:$port" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
    Write-Host ""
    
    # Set environment variables if needed
    $env:FLASK_APP = "app.main:app"
    $env:FLASK_ENV = "development"
    
    python run_local.py
}
