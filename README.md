# Cold Email Generator

> An AI-powered Chrome extension that extracts job postings from any webpage and instantly generates personalized cold emails — sent directly from your Gmail via SMTP.

**Built by [Anup Dutta](mailto:anup.analyst@gmail.com) · Python · FastAPI · LangChain · GROQ · ChromaDB**

---

## What It Does

```
Visit job posting  →  Click extension  →  AI extracts job details
       →  AI writes personalized email  →  One click to send via Gmail
```

Turn a 30-minute application into a 30-second one.

---

## Features

| Feature | Details |
|---|---|
| 🤖 **AI Extraction** | Scrapes and parses job details from any website |
| ✉️ **Email Generation** | Personalized emails via Llama 3.1 (GROQ) |
| 📎 **Resume Upload** | Upload your PDF resume; AI auto-generates your portfolio |
| 🔍 **Portfolio Matching** | ChromaDB vector search finds relevant projects for each job |
| 📤 **SMTP Sending** | Sends directly from Gmail — no OAuth dance, just an App Password |
| 🌐 **Universal** | Works on LinkedIn, Indeed, company career pages, and more |

---

## Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** — REST API server
- **[LangChain](https://www.langchain.com/)** + **[GROQ](https://console.groq.com/)** — LLM orchestration (Llama 3.1)
- **[ChromaDB](https://www.trychroma.com/)** — Vector database for semantic portfolio matching
- **smtplib** — Gmail sending via App Password (no OAuth required)
- **PyMuPDF / pdfplumber** — Resume PDF parsing

### Frontend
- **Chrome Extension** (Manifest V3)
- Vanilla JavaScript · HTML · CSS

---

## Project Structure

```
Cold Email Generator/
├── main.py                        # FastAPI server — entry point (run this!)
├── requirements.txt               # All Python dependencies
├── venv/                          # Python virtual environment (not committed)
├── .env                           # Your secrets go here (not committed)
│
├── backend/                       # Core service modules
│   ├── smtp_service.py            # Gmail SMTP email sender
│   ├── resume_processor.py        # PDF resume parser → portfolio JSON
│   ├── resumes/                   # Uploaded PDF resumes (not committed)
│   └── vectorstore/               # ChromaDB data (not committed)
│
├── App/                           # LangChain logic + Streamlit UI
│   ├── CMGmain.py                 # Streamlit app (alternative front-end)
│   ├── CMGchain.py                # LangChain prompt chains
│   ├── CMGportfolio.py            # Portfolio query via ChromaDB
│   ├── CMGutils.py                # Text cleaning utilities
│   └── Resource/
│       └── my_portfolio.csv       # Fallback portfolio (tech stack + links)
│
├── extension/                     # Chrome extension (Manifest V3)
│   ├── manifest.json              # Extension config
│   ├── popup.html / popup.js      # Extension UI & logic
│   ├── content.js                 # Page scraper (runs on job sites)
│   ├── background.js              # Service worker
│   ├── config.js                  # API base URL config
│   └── icons/                     # Extension icons
│
├── Useless/                       # Archived / unused files (safe to ignore)
│   ├── docs/                      # Old setup guides & markdown docs
│   ├── notebooks/                 # Jupyter notebooks (prototypes)
│   ├── app_unused/                # Old Streamlit draft
│   ├── backend_unused/            # Old backend scripts
│   └── root_scripts/              # One-off utility scripts
│
├── Anup Dutta Resume.pdf          # Source resume
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites

- Python 3.8+
- Google Chrome
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords)
- A free [GROQ API key](https://console.groq.com/)

### 1 — Clone & Install

```bash
git clone <your-repo-url>
cd "Cold Emaill Generator"

# Create & activate virtual environment (from project root)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

### 2 — Configure Environment

Create `.env` in the **project root**:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Required for email sending
SMTP_EMAIL=your.gmail@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx   # 16-char Gmail App Password

# Optional
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_NAME=Your Name
```

> **Getting a Gmail App Password:**
> 1. Enable 2-Step Verification on your Google account
> 2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
> 3. Create a password for "Mail" — copy the 16 characters into `.env`

### 3 — Start the Server

```bash
# From the project root (with venv activated)
python main.py
# API running at http://localhost:8000
# Docs at       http://localhost:8000/docs
```

### 4 — Load the Chrome Extension

1. Open `chrome://extensions/`
2. Enable **Developer mode** (top-right toggle)
3. Click **Load unpacked** → select the `extension/` folder
4. Pin the extension to your toolbar

### 5 — Upload Your Resume *(optional but recommended)*

In the extension popup, click **Upload Resume** and upload your PDF.  
The AI will extract your skills, experience, and projects and use them to personalize every email.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/extract-job` | Extract structured job data from raw page text |
| `POST` | `/api/generate-email` | Generate a personalized cold email |
| `POST` | `/api/send-email-smtp` | Send the email via Gmail SMTP |
| `GET` | `/api/smtp-status` | Check SMTP configuration |
| `POST` | `/api/upload-resume` | Upload PDF resume & rebuild portfolio |
| `GET` | `/api/resume-status` | Check if a resume has been uploaded |
| `GET` | `/api/portfolio` | View current parsed portfolio |
| `DELETE` | `/api/resume` | Remove resume & reset portfolio |
| `GET` | `/health` | Server health check |

Interactive docs available at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

---

## Customization

### Portfolio (no resume)

If you prefer not to upload a PDF, edit `App/Resource/my_portfolio.csv` directly:

```csv
"Techstack","Links"
"Python, Machine Learning","https://github.com/you/ml-project"
"React, TypeScript","https://github.com/you/react-app"
"SQL, Data Analysis","https://github.com/you/data-project"
```

### Email Style & Tone

Edit the LangChain prompts in `App/CMGchain.py` to adjust the email's tone, structure, or professional summary.

### Production Deployment

Update `API_BASE_URL` in `extension/popup.js` to your deployed backend URL:

```javascript
// extension/popup.js  (line 2)
const API_BASE_URL = 'https://your-api.onrender.com';
```

**Recommended free hosts:** [Render](https://render.com) · [Railway](https://railway.app)

```bash
# Render start command
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Troubleshooting

**Server won't start**
```bash
# From project root
venv\Scripts\activate
pip install -r requirements.txt
# Confirm .env exists at project root with GROQ_API_KEY
```

**SMTP not sending**
- Confirm 2-Step Verification is ON for your Google account
- Verify the App Password in `.env` has no extra spaces
- Check `GET /api/smtp-status` for a diagnostic response

**Extension not working**
- Confirm the backend is running: [http://localhost:8000/health](http://localhost:8000/health)
- Open DevTools on the popup (right-click → Inspect) and check the console

**"Module not found" errors**
```bash
# Make sure the virtual environment is activated before starting
venv\Scripts\activate
python main.py
```

---

## Costs

| Service | Cost | Notes |
|---------|------|-------|
| GROQ API | **Free** | Generous rate limits for personal use |
| Gmail SMTP | **Free** | Up to 500 emails/day via App Password |
| Backend hosting | **Free** | Render / Railway free tiers |
| **Total** | **$0** | |

---

## Security & Privacy

- All credentials stay in your local `.env` file — nothing is committed to git
- SMTP App Passwords are limited to sending only; they cannot read your inbox
- The extension only reads the active tab's page content when you click it
- No user data is stored or transmitted to third parties beyond GROQ for LLM inference

---

## Roadmap

- [ ] Application tracking dashboard
- [ ] Follow-up email scheduling
- [ ] Multiple Gmail account support
- [ ] Company research integration
- [ ] Email template library (by role / seniority)

---

## License

MIT — free to fork, customize, and use for your own job search.

---

*Made with ❤️ and ☕ by [Anup Dutta](mailto:anup.analyst@gmail.com)*
