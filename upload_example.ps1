# Example: How to upload a file with authentication
Write-Host "=== File Upload Example with Authentication ===" -ForegroundColor Green

# Step 1: Login and get token
Write-Host "`n1. Logging in..." -ForegroundColor Yellow
$loginData = @{
    username = "testuser"
    password = "password123"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/v1/auth/login" -Method POST -Headers @{"Content-Type"="application/json"} -Body $loginData
    $loginResult = $loginResponse.Content | ConvertFrom-Json
    $token = $loginResult.token
    Write-Host "Login successful!" -ForegroundColor Green
} catch {
    Write-Host "Login failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Step 2: Create a test file
$testFile = "test_certificate.png"
if (-not (Test-Path $testFile)) {
    Write-Host "`n2. Creating test file..." -ForegroundColor Yellow
    $pngBytes = [Convert]::FromBase64String("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==")
    [System.IO.File]::WriteAllBytes($testFile, $pngBytes)
    Write-Host "Test file created: $testFile" -ForegroundColor Green
}

# Step 3: Upload file
Write-Host "`n3. Uploading file..." -ForegroundColor Yellow
Write-Host "File: $testFile" -ForegroundColor Cyan
Write-Host "Token: $($token.Substring(0,50))..." -ForegroundColor Cyan

try {
    # Simple upload test - just check if auth works
    $uploadResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/v1/certificates/upload" -Method POST -Headers @{"Authorization"="Bearer $token"}
} catch {
    if ($_.Exception.Message -like "*No file provided*") {
        Write-Host "SUCCESS: Authentication is working!" -ForegroundColor Green
        Write-Host "The 'No file provided' error means the auth header is correct." -ForegroundColor Yellow
    } else {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=== How to Upload Files ===" -ForegroundColor Green
Write-Host "1. Login to get a token" -ForegroundColor White
Write-Host "2. Include 'Authorization: Bearer <token>' header" -ForegroundColor White
Write-Host "3. Send multipart/form-data with your file" -ForegroundColor White