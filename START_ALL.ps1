# Master script to start all required services
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Certificate Verifier - Full System Startup" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$rootDir = $PSScriptRoot

# Function to start a service in a new window
function Start-ServiceWindow {
    param(
        [string]$Title,
        [string]$ScriptPath,
        [string]$Color
    )
    
    Write-Host "Starting $Title..." -ForegroundColor $Color
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { Set-Location '$rootDir'; $ScriptPath }"
    
    Start-Sleep -Seconds 2
}

Write-Host "📋 System Requirements Check:" -ForegroundColor Yellow
Write-Host "   1. Python installed" -ForegroundColor Gray
Write-Host "   2. Node.js installed" -ForegroundColor Gray
Write-Host "   3. All dependencies installed" -ForegroundColor Gray
Write-Host ""

# Check if university portal is already running
Write-Host "Checking existing services..." -ForegroundColor Yellow

$port3000 = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
$port5000 = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue
$port5173 = Get-NetTCPConnection -LocalPort 5173 -ErrorAction SilentlyContinue

if ($port3000) {
    Write-Host "✓ University Portal already running on port 3000" -ForegroundColor Green
} else {
    Start-ServiceWindow "University Portal (Port 3000)" ".\start-university-portal.ps1" "Cyan"
}

if ($port5000) {
    Write-Host "✓ Backend already running on port 5000" -ForegroundColor Green
} else {
    Start-ServiceWindow "Main Backend (Port 5000)" ".\start-backend.ps1" "Blue"
}

Start-Sleep -Seconds 3

if ($port5173) {
    Write-Host "✓ Frontend already running on port 5173" -ForegroundColor Green
} else {
    Write-Host "Starting Frontend (Port 5173)..." -ForegroundColor Magenta
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& { Set-Location '$rootDir\frontend'; npm run dev }"
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  All Services Started!" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application at:" -ForegroundColor Yellow
Write-Host "  🌐 Frontend:          http://localhost:5173" -ForegroundColor White
Write-Host "  🔧 Main Backend:      http://localhost:5000" -ForegroundColor White
Write-Host "  🎓 University Portal: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Database Status:" -ForegroundColor Yellow
$dbPath = Join-Path $rootDir "university-portal\database\certificates.json"
if (Test-Path $dbPath) {
    $dbContent = Get-Content $dbPath | ConvertFrom-Json
    $certCount = $dbContent.certificates.Count
    Write-Host "  ✓ Certificates in DB: $certCount" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Database file not found" -ForegroundColor Red
}
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
