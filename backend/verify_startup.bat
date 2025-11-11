@echo off
REM Startup verification script for Meeting Management System (Windows)

echo.
echo ========================================
echo Meeting Management System
echo Startup Verification
echo ========================================
echo.

REM Test 1: ORM Relationships
echo [Test 1] Verifying ORM relationships...
python test_orm_relationships.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAILED] ORM relationships test failed
    exit /b 1
)
echo [PASSED] ORM relationships test passed
echo.

echo ========================================
echo All verification tests passed!
echo ========================================
echo.
echo You can now start the server with:
echo   uvicorn app.main:app --reload
echo.
