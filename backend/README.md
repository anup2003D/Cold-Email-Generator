# 🚀 Cold Email Generator - Backend API

AI-powered backend API for automated cold email generation and Gmail integration.

## 📋 Prerequisites

- Python 3.8 or higher
- GROQ API Key
- Gmail API credentials (already set up in `../gmail_credentials.json`)

## 🛠️ Installation

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit `.env` and add your GROQ API key:

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

## 🚀 Running the Server

### Development Mode (Local)

```bash
python main.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Interactive API documentation)
- **Health Check**: http://localhost:8000/health

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📡 API Endpoints

### 1. Extract Job Information

**POST** `/api/extract-job`

Extract job details from scraped text.

```json
{
  "text": "Job posting text here..."
}
```

Response:
```json
{
  "success": true,
  "jobs": [{
    "role": "Data Analyst",
    "company_name": "TechCorp",
    "experience": "2-4 years",
    "skills": "Python, SQL, Tableau",
    "description": "...",
    "requirements": "..."
  }],
  "count": 1
}
```

### 2. Generate Cold Email

**POST** `/api/generate-email`

Generate personalized cold email.

```json
{
  "job_data": {
    "role": "Data Analyst",
    "company_name": "TechCorp",
    "skills": "Python, SQL"
  },
  "custom_links": ["https://portfolio.com/project1"]
}
```

Response:
```json
{
  "success": true,
  "email": "Generated email content...",
  "subject": "Application for Data Analyst - Anup",
  "job_role": "Data Analyst"
}
```

### 3. Get Gmail Authorization URL

**GET** `/api/gmail-auth-url`

Get OAuth URL for Gmail authorization.

Response:
```json
{
  "success": true,
  "auth_url": "https://accounts.google.com/o/oauth2/auth?..."
}
```

### 4. Handle Gmail OAuth Callback

**POST** `/api/gmail-callback`

Exchange authorization code for tokens.

```json
{
  "auth_code": "authorization_code_here"
}
```

Response:
```json
{
  "success": true,
  "access_token": "ya29...",
  "refresh_token": "1//...",
  "expires_in": "2024-03-15T10:30:00"
}
```

### 5. Send Email via Gmail

**POST** `/api/send-email`

Send email through Gmail API.

```json
{
  "to_email": "hiring@company.com",
  "subject": "Application for Data Analyst",
  "body": "Email content...",
  "access_token": "ya29..."
}
```

Response:
```json
{
  "success": true,
  "message_id": "18d4f5a2b3c1d9e7",
  "message": "Email sent successfully!"
}
```

## 🧪 Testing the API

### Using the Interactive Docs

Visit http://localhost:8000/docs to test all endpoints interactively.

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Extract job
curl -X POST http://localhost:8000/api/extract-job \
  -H "Content-Type: application/json" \
  -d '{"text": "Your job posting text"}'
```

## 📁 Project Structure

```
backend/
├── main.py              # FastAPI application
├── gmail_service.py     # Gmail API integration
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## 🔒 Security Notes

1. **Never commit `.env` file** - Contains sensitive API keys
2. **Gmail credentials** - Stored securely in parent directory
3. **CORS** - Configure properly for production deployment
4. **Access tokens** - Implement token refresh mechanism

## 🌐 Deployment

### Deploy to Render

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Create new "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**: Add `GROQ_API_KEY`
6. Deploy!

### Deploy to Railway

1. Install Railway CLI: `npm install -g railway`
2. Login: `railway login`
3. Initialize: `railway init`
4. Deploy: `railway up`
5. Add environment variables in Railway dashboard

## 🐛 Troubleshooting

### Import Errors

Make sure you're in the backend directory and have activated the virtual environment.

### Port Already in Use

Change the port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use different port
```

### Gmail API Errors

- Verify credentials file exists
- Check OAuth scopes are correct
- Ensure test user is added in Google Cloud Console

### GROQ API Errors

- Verify API key is correct
- Check API quota/limits
- Ensure proper internet connection

## 📞 Support

For issues or questions:
- Check the main project README
- Review API documentation at `/docs`
- Check logs for error details

---

Made with ❤️ by Anup
