# 🔧 Fixing Gmail OAuth Error: "invalid_client - Unauthorized"

## ❌ The Error:
```json
{"detail":"OAuth callback failed: (invalid_client) Unauthorized"}
```

## 🎯 Root Cause:
The **redirect URI in your code doesn't match** what's in Google Cloud Console.

---

## ✅ Solution:

### Step 1: Check Your Current Redirect URI

**Open:** `backend/gmail_service.py`

You'll see:
```python
self.REDIRECT_URI = 'http://localhost:8000/api/gmail-callback'
```

**This MUST EXACTLY match** what's in Google Cloud Console!

---

### Step 2: Update Google Cloud Console

1. **Go to:** https://console.cloud.google.com/apis/credentials

2. **Click your OAuth 2.0 Client ID** (the one you created earlier)

3. **Scroll to "Authorized redirect URIs"**

4. **Check if this URI exists:**
   ```
   http://localhost:8000/api/gmail-callback
   ```

5. **If NOT there:**
   - Click **"+ ADD URI"**
   - Paste: `http://localhost:8000/api/gmail-callback`
   - Click **"SAVE"**

6. **Wait 5-10 minutes** for Google to propagate changes

---

### Step 3: Verify Your gmail_credentials.json

**Check:** `gmail_credentials.json` in your project root

Make sure it has:
```json
{
  "web": {
    "client_id": "466718847603-pbj40i55mhggpqinr843nsh49gc2n19s.apps.googleusercontent.com",
    "client_secret": "YOUR_SECRET_HERE",
    ...
  }
}
```

If it says `"installed"` instead of `"web"`, that's wrong! You need a **Web Application** OAuth client, not a Desktop app.

---

## 🔄 Alternative: Use SMTP Instead!

**Much simpler - no OAuth needed!**

See [SMTP_SETUP.md](SMTP_SETUP.md) for easy email sending without this OAuth complexity.

---

## 📋 Complete Checklist:

- [ ] Backend running on `http://localhost:8000`
- [ ] Redirect URI in `gmail_service.py` is `http://localhost:8000/api/gmail-callback`
- [ ] Same URL added to Google Cloud Console redirect URIs
- [ ] Waited 5-10 minutes after saving in Google Console
- [ ] Using **Web Application** OAuth client (not Desktop)
- [ ] `gmail_credentials.json` file exists and is correct

---

## 🧪 Test the OAuth Flow:

**Step 1: Get auth URL**
```
GET http://localhost:8000/api/gmail-auth-url
```

**Step 2: Visit the URL in browser**
- Sign in
- Grant permissions
- You'll be redirected to: `http://localhost/?code=4/0A...`

**Step 3: Extract the code**
From the URL: `?code=4/0A...&scope=...`  
Copy only the code part (before `&`)

**Step 4: Exchange for tokens**
```
POST http://localhost:8000/api/gmail-callback

{
  "auth_code": "4/0A_YOUR_CODE_HERE"
}
```

**If successful:**
```json
{
  "success": true,
  "access_token": "ya29...",
  "refresh_token": "1//...",
  "expires_in": 3599
}
```

---

## 💡 Pro Tip:

For testing, **use SMTP** instead of Gmail API:
- No OAuth needed
- No redirect URI issues
- Just email + app password
- Works immediately

See [SMTP_SETUP.md](SMTP_SETUP.md) for setup!
