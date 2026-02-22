# Quick Start Instructions

## 🚀 Three Ways to Get Started

### Method 1: Automated Setup (Windows)

Double-click `start.bat` - it will:
- Check Python installation
- Create virtual environment
- Install dependencies
- Start the backend server

### Method 2: Manual Setup

```bash
# 1. Setup backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Create .env file
# Add: GROQ_API_KEY=your_key_here

# 3. Start server
python main.py

# 4. Load extension in Chrome
# Go to chrome://extensions/
# Enable Developer mode
# Load unpacked -> select 'extension' folder
```

### Method 3: Read Full Guide

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete instructions.

## ⚡ Next Steps

1. ✅ Backend running at http://localhost:8000
2. ✅ Load extension in Chrome
3. ✅ Connect Gmail account
4. ✅ Start applying to jobs!

## 📞 Need Help?

- Backend setup: See [backend/README.md](backend/README.md)
- Extension setup: See [extension/README.md](extension/README.md)
- Full guide: See [SETUP_GUIDE.md](SETUP_GUIDE.md)
