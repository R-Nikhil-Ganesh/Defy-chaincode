@echo off
echo ===================================================
echo   FRESHCHAIN TEAM SETUP INSTALLER
echo ===================================================

echo.
echo [1/2] Installing Blockchain Dependencies (Node.js)...
cd blockchain
call npm install
if %errorlevel% neq 0 (
    echo FAIL: Could not install Node dependencies. Do you have Node.js installed?
    pause
    exit /b
)
echo SUCCESS: Blockchain ready.

echo.
echo [2/2] Setting up Python Environment...
cd ..\backend

:: Check if venv exists, if not create it
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate and install
call venv\Scripts\activate
echo Installing Python libraries from requirements.txt...
pip install -r requirements.txt

echo.
echo ===================================================
echo   SETUP COMPLETE!
echo ===================================================
echo.
echo You can now run 'start_freshchain.bat' to launch the app.
pause