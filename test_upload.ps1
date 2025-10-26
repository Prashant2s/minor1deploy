# Test file upload with authentication
param(
    [string]$FilePath = "test_certificate.png",
    [string]$Username = "testuser",
    [string]$Password = "password123"
)

Write-Host "Testing file upload with authentication..."

# Step 1: Login to get token
Write-Host "1. Logging in to get authentication token..."
try {
    $loginBody = @{
        username = $Username
        password = $Password
    } | ConvertTo-Json
    
    $loginResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/v1/auth/login" `
        -Method POST `
        -Headers @{"Content-Type"="application/json"} `
        -Body $loginBody
    
    $loginData = $loginResponse.Content | ConvertFrom-Json
    $token = $loginData.token
    Write-Host "✓ Login successful! Token: $($token.Substring(0,50))..."
} catch {
    Write-Host "✗ Login failed: $($_.Exception.Message)"
    exit 1
}

# Step 2: Test file upload
Write-Host "2. Uploading file with authentication..."
try {
    # Check if file exists
    if (-not (Test-Path $FilePath)) {
        Write-Host "✗ File not found: $FilePath"
        exit 1
    }
    
    # Create multipart form data
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
    $bodyLines = (
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"$FilePath`"",
        "Content-Type: image/png",
        "",
        [System.IO.File]::ReadAllText($FilePath, [System.Text.Encoding]::UTF8),
        "--$boundary--",
        ""
    ) -join $LF
    
    $uploadResponse = Invoke-WebRequest -Uri "http://localhost:5000/api/v1/certificates/upload" `
        -Method POST `
        -Headers @{
            "Authorization" = "Bearer $token"
            "Content-Type" = "multipart/form-data; boundary=$boundary"
        } `
        -Body $bodyLines
    
    $uploadData = $uploadResponse.Content | ConvertFrom-Json
    Write-Host "✓ File upload successful!"
    Write-Host "Certificate ID: $($uploadData.certificate_id)"
    Write-Host "Status: $($uploadData.status)"
    
} catch {
    Write-Host "✗ File upload failed: $($_.Exception.Message)"
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody"
    }
}

Write-Host "Test completed!"
