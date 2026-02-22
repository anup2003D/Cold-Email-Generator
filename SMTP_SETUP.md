# 📧 SMTP Email Setup Guide

**SMTP is now available as a simpler alternative to Gmail API!**  
✅ No OAuth flow needed  
✅ No Google Cloud Console setup  
✅ Just email + app password  

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Gmail App Password

1. **Go to:** https://myaccount.google.com/apppasswords

2. **Sign in** to your Gmail account

3. **Click "Select app"** → Choose **"Mail"**

4. **Click "Select device"** → Choose **"Other"** → Type: `Cold Email Generator`

5. **Click "Generate"**

6. **Copy the 16-character password** (example: `abcd efgh ijkl mnop`)

---

### Step 2: Add to .env File

**Open:** `backend/.env` and add:

```dotenv
# SMTP Configuration
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_SENDER_NAME=Anup Dutta
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Replace:**
- `your-email@gmail.com` with your actual Gmail
- `abcdefghijklmnop` with your app password (remove spaces)
- `Anup Dutta` with your name

---

### Step 3: Restart Backend

```bash
# Stop server (Ctrl+C)
python main.py
```

---

### Step 4: Test SMTP

**Check status:**
```
GET http://localhost:8000/api/smtp-status
```

**Response (if configured correctly):**
```json
{
  "success": true,
  "configured": true,
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "your-email@gmail.com",
  "message": "SMTP is configured and ready to send emails"
}
```

---

## 📮 Sending Emails via SMTP

### In Postman:

```
POST http://localhost:8000/api/send-email-smtp
Content-Type: application/json

{
  "to_email": "recipient@example.com",
  "subject": "Application for Data Analyst - Anup",
  "body": "Dear Hiring Manager,\n\nI am writing to apply..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "Email sent successfully to recipient@example.com",
  "method": "SMTP"
}
```

---

## 🎯 Using SMTP in Extension

The extension will automatically use SMTP if you update the send email function.

**Update `extension/popup.js`** - find the `sendEmail` function and change the endpoint:

```javascript
// Change from:
const response = await fetch(`${API_BASE_URL}/api/send-email`, {

// To:
const response = await fetch(`${API_BASE_URL}/api/send-email-smtp`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        to_email: recipientEmail.value,
        subject: emailSubject,
        body: generatedEmail
        // Note: No access_token needed for SMTP!
    })
});
```

---

## 🔄 Gmail API vs SMTP

| Feature | Gmail API (OAuth) | SMTP |
|---------|------------------|------|
| Setup complexity | Complex (OAuth flow) | Simple (email + password) |
| Google Cloud Console | Required | Not needed |
| Extension integration | Complex redirect handling | Direct API call |
| Security | OAuth tokens | App password |
| Best for | Production | Testing/Development |

---

## ⚠️ Troubleshooting

### "SMTP Authentication failed"
- ✅ Make sure you're using **App Password**, not your Gmail password
- ✅ Remove spaces from app password: `abcd efgh ijkl mnop` → `abcdefghijklmnop`
- ✅ Check "Less secure app access" is NOT needed (App Passwords work regardless)

### "SMTP not configured"
- ✅ Check `.env` file has `SMTP_EMAIL` and `SMTP_PASSWORD`
- ✅ Restart backend after adding credentials
- ✅ Check for typos in variable names

### Emails not arriving
- ✅ Check spam folder
- ✅ Verify recipient email is correct
- ✅ Wait a few minutes (SMTP can be delayed)

---

## 🎉 Benefits

✅ **No OAuth errors** - Skip the complex Gmail API setup  
✅ **Instant testing** - Send emails immediately  
✅ **Simple integration** - Just 3 fields needed  
✅ **Works everywhere** - No redirect URI issues  

**Perfect for testing your cold email generator!** 🚀

---

## 📝 API Endpoints

### Check SMTP Status
```
GET /api/smtp-status
```

### Send Email via SMTP
```
POST /api/send-email-smtp
Body: { "to_email", "subject", "body" }
```

### Send Email via Gmail API (original)
```
POST /api/send-email
Body: { "to_email", "subject", "body", "access_token" }
```

---

Need help? The SMTP service is in `backend/smtp_service.py`
