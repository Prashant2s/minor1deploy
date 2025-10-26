@echo off
echo ========================================
echo   Docker Refresh Script for Windows
echo ========================================
echo.

echo [1/4] Stopping containers...
docker-compose down

echo.
echo [2/4] Rebuilding images with latest changes...
docker-compose build --no-cache

echo.
echo [3/4] Starting containers in detached mode...
docker-compose up -d

echo.
echo [4/4] Checking container status...
docker-compose ps

echo.
echo ========================================
echo   Docker refresh complete!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:5000
echo ========================================
echo.

pause