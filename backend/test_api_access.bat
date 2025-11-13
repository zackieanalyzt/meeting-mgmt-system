@echo off
REM Test API access with admin_group role (Windows)

echo.
echo ========================================
echo Testing API Access with admin_group Role
echo ========================================
echo.

set BASE_URL=http://localhost:8000

REM Test 1: Login
echo [Test 1] Login as group_admin
curl -s -X POST "%BASE_URL%/api/v1/auth/login" ^
  -H "Content-Type: application/x-www-form-urlencoded" ^
  -d "username=group_admin&password=any" > login_response.json

REM Extract token (simplified for Windows)
echo [INFO] Check login_response.json for token
echo.

REM Test 2: Manual verification
echo [Test 2] Manual Verification Steps:
echo 1. Open http://localhost:8000/docs
echo 2. Click "Authorize" button
echo 3. Login with: group_admin / any
echo 4. Try GET /api/v1/meetings
echo 5. Should return 200 OK (not 403)
echo.

echo ========================================
echo Please verify manually in Swagger UI
echo ========================================
echo.

del login_response.json 2>nul
