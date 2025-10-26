@echo off
echo ========================================
echo   Quick Docker Refresh (with cache)
echo ========================================
echo.

echo [1/3] Stopping containers...
docker-compose down

echo.
echo [2/3] Rebuilding and starting containers...
docker-compose up --build -d

echo.
echo [3/3] Checking status...
docker-compose ps

echo.
echo ========================================
echo   Quick refresh complete!
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:5000
echo ========================================