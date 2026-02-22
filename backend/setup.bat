@echo off
echo ========================================
echo Backend Setup - Installing Dependencies
echo ========================================
echo.

cd /d "%~dp0"

echo [Step 1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✓ Python found
echo.

echo [Step 2/4] Creating virtual environment...
if exist "venv" (
    echo ✓ Virtual environment already exists
) else (
    python -m venv venv
    echo ✓ Virtual environment created
)
echo.

echo [Step 3/4] Activating virtual environment...
call venv\Scripts\activate
echo ✓ Virtual environment activated
echo.

echo [Step 4/4] Installing dependencies (FastAPI, uvicorn, etc.)...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Try running manually:
    echo   cd backend
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)
echo.
echo ✓ All dependencies installed successfully!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo FastAPI and all modules are now installed in the virtual environment.
echo.
echo Next steps:
echo 1. Create .env file with your GROQ_API_KEY
echo 2. Run: python main.py
echo.
echo Or just run: ..\start.bat (from parent folder)
echo.
pause
