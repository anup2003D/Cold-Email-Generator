# 📧 Cold Email Generator - Complete Setup Guide

Automated cold email generation system with browser extension and Gmail integration.

## 🎯 System Overview

```
Browser Extension → Backend API → AI (GROQ) + Portfolio Matching → Gmail API → Send Email
```

**What This Does:**
1. Extracts job postings from websites
2. Generates personalized application emails using AI
3. Sends emails directly from your Gmail account
4. All with just a few clicks!

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.8+ installed
- [ ] Google Chrome or Microsoft Edge browser
- [ ] GROQ API Key ([Get it free here](https://console.groq.com/))
- [ ] Gmail account
- [ ] Google Cloud Console setup completed (see below)

---

## 🚀 Quick Start Guide

### Phase 1: Backend Setup (10 minutes)

#### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

#### 2. Configure Environment

Create `.env` file in `backend/` folder:

```bash
GROQ_API_KEY=your_groq_api_key_here
```

**Where to get GROQ API Key:**
1. Go to https://console.groq.com/
2. Sign up for free
3. Navigate to API Keys
4. Create new key
5. Copy and paste into `.env` file

#### 3. Start Backend Server

```bash
python main.py
```

You should see:
```
Starting Cold Email Generator API...
API Documentation: http://localhost:8000/docs
```

**✅ Keep this terminal window open!**

---

### Phase 2: Extension Setup (5 minutes)

#### 1. Load Extension in Chrome

1. Open Chrome
2. Go to: `chrome://extensions/`
3. Enable **"Developer mode"** (top-right toggle)
4. Click **"Load unpacked"**
5. Select the `extension` folder from this project
6. Extension icon appears in toolbar!

#### 2. Add Extension Icons (Optional)

The extension works without icons, but looks better with them.

Create three PNG files in `extension/icons/`:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

**Quick way:** Use any purple/gradient square images for testing.

---

### Phase 3: Gmail Connection (5 minutes)

#### 1. In Extension:

1. Click extension icon in Chrome toolbar
2. Click **"Connect Gmail Account"**
3. New tab opens with Google sign-in
4. Choose your Gmail account
5. Click **"Allow"** to grant permissions
6. Tab closes automatically
7. Extension shows **"✅ Gmail Connected"**

#### 2. Troubleshooting Gmail Connection:

If you see an "unverified app" warning:
1. Click **"Advanced"**
2. Click **"Go to Cold Email Generator (unsafe)"** 
3. This is normal for personal projects
4. Click **"Allow"**

---

## 🎉 You're Ready! How to Use

### Complete Workflow:

1. **Navigate to a job posting** (LinkedIn, Indeed, company site)
2. **Click extension icon**
3. **Click "Extract Job from Current Page"**
   - Waits 2-3 seconds
   - Job details appear
4. **Click "Generate Cold Email"**
   - Waits 2-3 seconds  
   - Personalized email appears
5. **Enter recipient email** (or use auto-detected)
6. **Click "🚀 Send Email"**
7. **✅ Done!** Email sent from your Gmail

---

## 📁 Project Structure

```
Cold Email Generator/
├── App/                          # Original Streamlit app
│   ├── CMGchain.py              # AI email generation
│   ├── CMGportfolio.py          # Portfolio matching
│   ├── CMGutils.py              # Text utilities
│   └── Resource/
│       └── my_portfolio.csv     # Your portfolio projects
│
├── backend/                      # FastAPI backend
│   ├── main.py                  # API server
│   ├── gmail_service.py         # Gmail integration
│   ├── requirements.txt         # Python dependencies
│   ├── .env                     # Your API keys (create this)
│   └── README.md                # Backend docs
│
├── extension/                    # Chrome extension
│   ├── manifest.json            # Extension config
│   ├── popup.html               # UI
│   ├── popup.js                 # Logic
│   ├── content.js               # Page scraping
│   ├── background.js            # Background tasks
│   ├── icons/                   # Extension icons
│   └── README.md                # Extension docs
│
├── gmail_credentials.json        # Google OAuth credentials
└── README.md                     # This file
```

---

## 🔧 Customization

### Update Your Portfolio

Edit `App/Resource/my_portfolio.csv`:

```csv
"Techstack","Links"
"Python, Machine Learning","https://github.com/yourusername/ml-project"
"React, TypeScript","https://github.com/yourusername/react-app"
```

### Customize Email Template

Edit email generation prompts in `App/CMGchain.py`, around line 90-180.

### Change Your Profile

Update your profile information in `App/CMGchain.py`:
- Work experience
- Skills
- Achievements
- Contact info

---

## 🌐 Deployment (Optional)

### Deploy Backend to Cloud

#### Option 1: Render (Recommended)

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Create "Web Service"
4. Connect GitHub repo
5. Configure:
   - **Build**: `pip install -r backend/requirements.txt`
   - **Start**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Add `GROQ_API_KEY`
6. Deploy!
7. Get your URL (e.g., `https://yourapp.onrender.com`)

#### Option 2: Railway

```bash
npm install -g railway
railway login
cd backend
railway init
railway up
```

### Update Extension for Production

Edit `extension/popup.js` line 2:

```javascript
const API_BASE_URL = 'https://your-deployed-api.com';
```

Reload extension in Chrome.

---

## 🐛 Common Issues & Solutions

### Backend Won't Start

**Error:** `ModuleNotFoundError`
- **Solution:** Make sure virtual environment is activated and dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

**Error:** `Port already in use`
- **Solution:** Change port in `backend/main.py`:
  ```python
  uvicorn.run(app, host="0.0.0.0", port=8001)
  ```

### Extension Not Working

**Issue:** Extension icon not appearing
- **Solution:** 
  1. Go to `chrome://extensions/`
  2. Enable "Developer mode"
  3. Reload the extension

**Issue:** "Failed to extract job"
- **Solution:**
  1. Make sure you're on an actual job posting page
  2. Check backend is running (`http://localhost:8000/health`)
  3. Check browser console for errors (right-click extension icon → Inspect)

### Gmail Issues

**Issue:** Can't connect Gmail
- **Solution:**
  1. Verify `gmail_credentials.json` exists
  2. Check Google Cloud Console setup
  3. Make sure OAuth scope `gmail.send` is added
  4. Try incognito mode

**Issue:** "Failed to send email"
- **Solution:**
  1. Reconnect Gmail (token might be expired)
  2. Check recipient email is valid
  3. Verify Gmail API quota not exceeded

### API Errors

**Issue:** CORS errors
- **Solution:** Make sure backend CORS is configured in `backend/main.py`

**Issue:** 500 Internal Server Error
- **Solution:** Check backend terminal for error logs

---

## 📊 Monitoring & Limits

### Gmail API Limits

- **Free quota:** 1 billion units/day
- **Sending 1 email:** ~100 units
- **Effective limit:** ~10,000 emails/day
- **For job hunting:** You'll never hit this limit!

### GROQ API Limits

- **Free tier:** Generous for personal use
- **Rate limit:** Usually sufficient
- **If exceeded:** Wait or upgrade plan

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to GitHub
2. **Keep `gmail_credentials.json` private**
3. **Use environment variables** for sensitive data
4. **Enable 2FA** on your Gmail account
5. **Review generated emails** before sending
6. **Regularly rotate API keys**

---

## 📈 Usage Analytics

Track your applications:
- Emails sent: Check Gmail "Sent" folder
- Response rate: Monitor your inbox
- Successful applications: Update your tracking sheet

---

## 🎓 Learning Resources

### Understanding the Tech Stack

- **FastAPI:** https://fastapi.tiangolo.com/
- **Chrome Extensions:** https://developer.chrome.com/docs/extensions/
- **Gmail API:** https://developers.google.com/gmail/api
- **LangChain:** https://python.langchain.com/
- **ChromaDB:** https://www.trychroma.com/

### Customization Ideas

- Add more portfolio projects
- Customize email templates
- Add email templates for different roles
- Track sent applications in a database
- Add email scheduling
- Create follow-up email templates

---

## 🤝 Contributing

This is your personal project! Feel free to:
- Modify the code to fit your needs
- Add new features
- Improve the UI
- Share with friends (with your own GROQ key)

---

## 📞 Getting Help

1. **Check the logs:**
   - Backend: Terminal where you ran `python main.py`
   - Extension: Right-click icon → Inspect popup → Console

2. **Review documentation:**
   - Backend: `backend/README.md`
   - Extension: `extension/README.md`

3. **Common fixes:**
   - Restart backend server
   - Reload extension
   - Clear browser cache
   - Check API keys are correct

---

## 🎯 Next Steps

Now that everything is set up:

1. ✅ Test on a few job postings
2. ✅ Customize your portfolio CSV
3. ✅ Adjust email templates to match your style
4. ✅ Start applying to jobs efficiently!
5. ✅ (Optional) Deploy to production for use anywhere

---

## 📝 Changelog

**Version 1.0.0** (Current)
- Initial release
- Backend API with FastAPI
- Chrome extension with Gmail integration
- AI-powered email generation
- Portfolio matching system

---

## ⭐ Features

- ✅ One-click job extraction
- ✅ AI-powered email generation
- ✅ Smart portfolio matching
- ✅ Direct Gmail sending
- ✅ Edit before sending
- ✅ Works on any job site
- ✅ Completely free to use
- ✅ Open source

---

## 🚀 Pro Tips

1. **Customize emails:** Always review and personalize before sending
2. **Target quality:** Better to send 10 great emails than 100 generic ones
3. **Follow up:** Track responses and follow up after 1-2 weeks
4. **A/B test:** Try different email styles to see what works
5. **Portfolio matters:** Keep your portfolio projects updated and relevant

---

**Happy Job Hunting! 🎉**

Made with ❤️ by Anup

---

## 📄 License

This is your personal project. Use it however you want!

---

## 🙏 Acknowledgments

- GROQ for fast LLM inference
- Google for Gmail API
- LangChain for LLM orchestration
- ChromaDB for vector search
- FastAPI for the awesome framework
