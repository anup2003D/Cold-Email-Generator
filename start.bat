@echo off
echo ========================================
echo Cold Email Generator - Quick Start
echo ========================================
echo.

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo.

echo [2/3] Starting Backend Server...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create backend\.env file with your GROQ_API_KEY
    echo.
    echo Example:
    echo GROQ_API_KEY=your_key_here
    echo.
    pause
)

echo Installing dependencies...
pip install -q -r requirements.txt

echo.
echo [3/3] Starting API server...
echo.
echo ========================================
echo Backend API is starting...
echo API Docs: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo ========================================
echo.
echo Next steps:
echo 1. Load extension in Chrome (chrome://extensions/)
echo 2. Enable Developer mode
echo 3. Click "Load unpacked" and select 'extension' folder
echo 4. Click extension icon and connect Gmail
echo 5. Start generating cold emails!
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python main.py
