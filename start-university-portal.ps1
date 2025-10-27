# Start University Portal on port 3000
Write-Host "🎓 Starting JUET University Portal..." -ForegroundColor Cyan
Write-Host ""

Set-Location -Path "university-portal\backend"

# Check if port 3000 is already in use
$port = 3000
$listener = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue

if ($listener) {
    Write-Host "⚠️  Port $port is already in use!" -ForegroundColor Yellow
    Write-Host "University portal may already be running." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To check: curl http://localhost:3000/health" -ForegroundColor Gray
} else {
    Write-Host "Starting Flask server on http://localhost:$port" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
    Write-Host ""
    
    python app.py
}
