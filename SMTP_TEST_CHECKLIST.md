# 📧 SMTP Testing Checklist

Follow these steps to test SMTP email sending:

## ✅ Step-by-Step Testing:

### 1. Get Gmail App Password ⏱️ 2 minutes
- [ ] Go to: https://myaccount.google.com/apppasswords
- [ ] Sign in with Gmail
- [ ] Select app: **Mail**
- [ ] Select device: **Other** → Type: `Cold Email Generator`
- [ ] Click **Generate**
- [ ] Copy the 16-character password (remove spaces!)

### 2. Add to .env File ⏱️ 1 minute
- [ ] Open: `backend/.env`
- [ ] Add these lines:
```dotenv
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=abcdefghijklmnop
SMTP_SENDER_NAME=Anup Dutta
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```
- [ ] Replace email and password with your actual credentials
- [ ] Save the file

### 3. Restart Backend ⏱️ 30 seconds
- [ ] Stop backend (Ctrl+C in terminal)
- [ ] Run: `python main.py`
- [ ] Wait for "Uvicorn running on http://localhost:8000"

### 4. Test SMTP Status ⏱️ 30 seconds
**In Postman or Browser:**
```
GET http://localhost:8000/api/smtp-status
```

**Expected Response:**
```json
{
  "success": true,
  "configured": true,
  "sender_email": "your-email@gmail.com",
  "message": "SMTP is configured and ready to send emails"
}
```

- [ ] Status shows "configured": true
- [ ] Sender email is correct

### 5. Send Test Email to Yourself ⏱️ 1 minute
**In Postman:**
```
POST http://localhost:8000/api/send-email-smtp
Content-Type: application/json

{
  "to_email": "YOUR-EMAIL@gmail.com",
  "subject": "🎉 SMTP Test - Cold Email Generator",
  "body": "This is a test email.\n\nIf you receive this, SMTP is working perfectly!\n\n✅ Backend: Connected\n✅ SMTP: Configured\n✅ Email Sending: Working\n\nYou're ready to send cold emails!"
}
```

- [ ] Response shows "success": true
- [ ] Check your inbox (or spam folder)
- [ ] Email received successfully

### 6. Test Complete Workflow ⏱️ 2 minutes

**Generate a real cold email:**

a) Extract job:
```
POST http://localhost:8000/api/extract-job

{
  "text": "We are hiring a Data Analyst with 3+ years experience in Python, SQL, and Tableau. Must have strong analytical skills and experience with data visualization. Send resume to careers@company.com"
}
```

b) Generate email:
```
POST http://localhost:8000/api/generate-email

{
  "job_data": {
    "role": "Data Analyst",
    "experience": "3+ years",
    "skills": "Python, SQL, Tableau",
    "description": "Data analysis and visualization",
    "requirements": "Strong analytical skills",
    "company_name": "TechCorp"
  }
}
```

c) Send the generated email:
```
POST http://localhost:8000/api/send-email-smtp

{
  "to_email": "YOUR-EMAIL@gmail.com",
  "subject": "Application for Data Analyst - Anup",
  "body": "[paste generated email from step b]"
}
```

- [ ] Job extracted successfully
- [ ] Email generated with personalized content
- [ ] Email sent and received

### 7. Test Extension ⏱️ 2 minutes

- [ ] Go to `chrome://extensions/`
- [ ] Find "Cold Email Generator"
- [ ] Click refresh icon (🔄)
- [ ] Visit a job posting website
- [ ] Click extension icon
- [ ] Click "Extract Job from Page"
- [ ] Click "Generate Email"
- [ ] Enter recipient email
- [ ] Click "🚀 Send Email"
- [ ] Check if email was sent successfully

---

## ✅ Success Criteria:

All of these should work:
- [x] SMTP status returns "configured": true
- [x] Test email received in inbox
- [x] Generated cold email looks professional
- [x] Email sent through extension works
- [x] No OAuth errors or authentication issues

---

## 🐛 Troubleshooting:

### "SMTP Authentication failed"
- ✅ Using App Password, not regular Gmail password?
- ✅ Removed all spaces from app password?
- ✅ Correct email address in SMTP_EMAIL?

### "SMTP not configured"
- ✅ Added credentials to `.env` file (not `.env.example`)?
- ✅ Restarted backend after adding credentials?
- ✅ No typos in variable names (SMTP_EMAIL, SMTP_PASSWORD)?

### Email not received
- ✅ Check spam/junk folder
- ✅ Wait a few minutes (SMTP can be delayed)
- ✅ Verify recipient email is correct
- ✅ Check backend terminal for error messages

### Extension not working
- ✅ Reloaded extension after code changes?
- ✅ Backend running on correct port?
- ✅ Extension API_BASE_URL is set to http://localhost:8000?

---

## 🎯 Once SMTP Works:

✅ **You're ready to use the extension!**

**Next Steps:**
1. Upload your resume via extension
2. Visit job postings
3. Extract job details
4. Generate personalized emails
5. Send applications!

**Gmail OAuth Setup (Optional - Later):**
- Only needed if you want to switch from SMTP to Gmail API
- Follow [GMAIL_OAUTH_FIX.md](GMAIL_OAUTH_FIX.md) when ready
- SMTP works perfectly for now!

---

## 📊 Time Estimate:
**Total Setup + Testing: ~10 minutes**

Good luck! 🚀
