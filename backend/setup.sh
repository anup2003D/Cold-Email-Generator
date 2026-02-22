#!/bin/bash
# Backend Setup Script for Mac/Linux

echo "========================================"
echo "Backend Setup - Installing Dependencies"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[Step 1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found! Please install Python 3.8+"
    exit 1
fi
echo "✓ Python found"
echo ""

echo "[Step 2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

echo "[Step 3/4] Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

echo "[Step 4/4] Installing dependencies (FastAPI, uvicorn, etc.)..."
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to install dependencies"
    echo "Try running manually:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi
echo ""
echo "✓ All dependencies installed successfully!"
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "FastAPI and all modules are now installed in the virtual environment."
echo ""
echo "Next steps:"
echo "1. Create .env file with your GROQ_API_KEY"
echo "2. Run: python main.py"
echo ""
