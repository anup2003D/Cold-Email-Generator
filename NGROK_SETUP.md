# 🌐 Ngrok Configuration Guide

Your project is now configured to use ngrok for public access!

## Current Ngrok URL
```
https://aridly-nonconstrictive-vella.ngrok-free.dev
```

## ✅ What's Been Updated:

1. **Extension API URL** ([extension/popup.js](extension/popup.js))
   - Changed from: `http://localhost:8000`
   - Changed to: `https://aridly-nonconstrictive-vella.ngrok-free.dev`

2. **Gmail OAuth Redirect URI** ([backend/gmail_service.py](backend/gmail_service.py))
   - Changed from: `http://localhost:8000/api/gmail-callback`
   - Changed to: `https://aridly-nonconstrictive-vella.ngrok-free.dev/api/gmail-callback`

3. **Config Reference** ([extension/config.js](extension/config.js))
   - Updated for documentation

## 🔧 IMPORTANT: Update Google Cloud Console

You **MUST** add the ngrok redirect URI to your Google Cloud OAuth settings:

### Steps:

1. **Go to:** https://console.cloud.google.com/apis/credentials

2. **Select your OAuth 2.0 Client ID** (the one you created earlier)

3. **Scroll to "Authorized redirect URIs"**

4. **Click "+ ADD URI"**

5. **Add this exact URL:**
   ```
   https://aridly-nonconstrictive-vella.ngrok-free.dev/api/gmail-callback
   ```

6. **Click "SAVE"**

7. **Wait 5 minutes** for changes to propagate

### Keep localhost too (optional):
You can keep `http://localhost:8000/api/gmail-callback` for local testing.

---

## 🚀 How to Use:

### Start Backend with Ngrok:

**Terminal 1 - Start Backend:**
```bash
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 2 - Start Ngrok:**
```bash
ngrok http 8000
```

Or if ngrok is already running, your backend should be accessible at:
```
https://aridly-nonconstrictive-vella.ngrok-free.dev
```

### Reload Extension:

1. Go to `chrome://extensions/`
2. Find "Cold Email Generator"
3. Click the **refresh icon** (🔄)

### Test the API:

```bash
# Test in browser or Postman:
GET https://aridly-nonconstrictive-vella.ngrok-free.dev/
```

Should return:
```json
{
  "message": "Cold Email Generator API",
  "version": "1.0.0",
  "endpoints": [...]
}
```

---

## 📱 Benefits of Ngrok:

✅ **Test from anywhere** - Share with friends or test on mobile  
✅ **HTTPS support** - Works with OAuth flows properly  
✅ **No firewall issues** - Bypasses network restrictions  
✅ **Professional testing** - Simulate production environment  

---

## ⚠️ Important Notes:

1. **Free ngrok URLs change** when you restart ngrok - you'll need to update:
   - `extension/popup.js` - API_BASE_URL
   - `backend/gmail_service.py` - REDIRECT_URI
   - Google Cloud Console - Authorized redirect URIs

2. **Paid ngrok plan** gives you a permanent subdomain (e.g., `your-app.ngrok.io`)

3. **For production**, deploy to a real server (AWS, Azure, Heroku, etc.)

---

## 🔄 Switching Back to Localhost:

If you want to use localhost again:

1. **Update popup.js:**
   ```javascript
   const API_BASE_URL = 'http://localhost:8000';
   ```

2. **Update gmail_service.py:**
   ```python
   self.REDIRECT_URI = 'http://localhost:8000/api/gmail-callback'
   ```

3. **Reload extension** in Chrome

---

## 🎯 Next Steps:

1. ✅ Add ngrok redirect URI to Google Cloud Console
2. ✅ Wait 5 minutes
3. ✅ Reload extension
4. ✅ Test OAuth flow with "Connect Gmail Account"
5. ✅ Test job extraction and email generation

Your extension is now publicly accessible! 🚀
