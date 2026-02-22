# 🔌 Cold Email Generator - Browser Extension

Chrome/Edge browser extension for automated cold email generation and sending.

## 📋 Prerequisites

- Google Chrome or Microsoft Edge browser
- Backend API running (see `../backend/README.md`)
- Gmail account connected

## 🚀 Installation (Development Mode)

### 1. Load Extension in Chrome

1. Open Chrome and go to: `chrome://extensions/`
2. Enable **"Developer mode"** (toggle in top-right corner)
3. Click **"Load unpacked"**
4. Navigate to and select the `extension` folder
5. The extension icon will appear in your toolbar! 🎉

### 2. Verify Installation

- Extension icon should be visible in Chrome toolbar
- Click the icon to open the popup
- You should see "Ready to generate cold emails!"

## 🎨 Adding Extension Icons

The extension needs icons to display properly. You have two options:

### Option 1: Quick Test Icons

Create simple colored squares for testing:

1. Use any image editor (Paint, Photoshop, etc.)
2. Create three PNG files:
   - `icons/icon16.png` (16x16 pixels)
   - `icons/icon48.png` (48x48 pixels)
   - `icons/icon128.png` (128x128 pixels)
3. Fill with purple/gradient color

### Option 2: Professional Icons

Use online tools:
- [Canva](https://www.canva.com/) - Free templates
- [Figma](https://www.figma.com/) - Design tool
- [Favicon.io](https://favicon.io/) - Icon generator

**Recommended design:**
- Purple gradient (#667eea to #764ba2)
- Email envelope symbol 📧
- Modern, minimal style

## 📖 How to Use

### Step 1: Start Backend Server

Make sure your backend API is running:

```bash
cd backend
python main.py
```

### Step 2: Connect Gmail

1. Click extension icon
2. Click **"Connect Gmail Account"**
3. Sign in with your Google account
4. Grant permissions
5. Extension shows "✅ Gmail Connected"

### Step 3: Extract Job Information

1. Navigate to any job posting page (LinkedIn, Indeed, company career pages)
2. Click extension icon
3. Click **"Extract Job from Current Page"**
4. Extension automatically scrapes and analyzes the job details
5. Review the extracted information

### Step 4: Generate Cold Email

1. Click **"Generate Cold Email"**
2. AI generates a personalized application email
3. Review the generated email
4. Click **"✏️ Edit"** if you want to make changes

### Step 5: Send Email

1. Enter recipient email address (or auto-detected from page)
2. Click **"🚀 Send Email"**
3. Confirm sending
4. ✅ Email sent!

## 🎯 Supported Websites

The extension works on most job posting sites:

- LinkedIn Jobs
- Indeed
- Glassdoor
- Company career pages
- Job board listings
- Direct job posting URLs

## ⚙️ Configuration

### Change Backend API URL

Edit `popup.js` line 2:

```javascript
const API_BASE_URL = 'http://localhost:8000';  // Change to your deployed API URL
```

For production deployment:
```javascript
const API_BASE_URL = 'https://your-api-domain.com';
```

### Customize Email Generation

The email generation logic is in the backend. Modify:
- `backend/CMGchain.py` - Email templates and prompts
- `backend/CMGportfolio.py` - Portfolio matching logic

## 📁 Extension Structure

```
extension/
├── manifest.json       # Extension configuration
├── popup.html         # Extension popup UI
├── popup.js           # Popup logic and API calls
├── content.js         # Page content extraction
├── background.js      # Background service worker
├── config.js          # Configuration
└── icons/             # Extension icons
    ├── icon16.png
    ├── icon48.png
    └── icon128.png
```

## 🔧 Development Tips

### Debug Extension

1. Right-click extension icon → "Inspect popup"
2. Chrome DevTools opens for debugging
3. Check Console for errors
4. Monitor Network tab for API calls

### Reload Extension After Changes

1. Go to `chrome://extensions/`
2. Click reload button (🔄) on your extension
3. Test changes

### View Logs

- **Popup logs**: Right-click icon → Inspect popup
- **Background logs**: chrome://extensions/ → Extension → Inspect views: background page
- **Content script logs**: F12 on any webpage

## 🌐 Publishing to Chrome Web Store (Optional)

### Prerequisites

- Chrome Web Store Developer account ($5 one-time fee)
- Extension icons and screenshots
- Privacy policy (if collecting data)

### Steps

1. Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole/)
2. Create new item
3. Upload extension ZIP file
4. Fill out store listing:
   - Name: "Cold Email Generator"
   - Description: Your app description
   - Screenshots: Extension UI screenshots
   - Category: Productivity
5. Submit for review (1-3 days)

### Before Publishing

- Test thoroughly
- Create proper icons
- Write clear description
- Add privacy policy
- Test on multiple websites

## 🔒 Security & Privacy

- Extension only runs when you click it (no automatic actions)
- Credentials stored locally in Chrome storage
- No data sent to third parties
- Open source - inspect the code yourself

## 🐛 Troubleshooting

### Extension Not Appearing

- Make sure Developer mode is enabled
- Try reloading the extension
- Check for errors in chrome://extensions/

### "Failed to Extract Job"

- Make sure you're on an actual job posting page
- Page might have anti-scraping protection
- Try refreshing the page
- Check if backend API is running

### Gmail Connection Failed

- Verify Google Cloud Console setup
- Check credentials file is in correct location
- Ensure scopes are configured correctly
- Try clearing Chrome storage and reconnecting

### API Errors

- Check backend server is running
- Verify API URL in popup.js
- Check CORS settings in backend
- Monitor backend logs for errors

### Email Not Sending

- Verify Gmail connection (token not expired)
- Check recipient email is valid
- Ensure backend has internet access
- Review Gmail API quotas

## 💡 Tips for Best Results

1. **Job Pages**: Works best on dedicated job posting pages
2. **Email Recipients**: Double-check email addresses before sending
3. **Customization**: Edit generated emails to add personal touch
4. **Testing**: Test on localhost before deploying to production
5. **Quotas**: Be mindful of Gmail sending limits (2000/day)

## 🔄 Updating the Extension

After making changes to extension files:

1. Save your changes
2. Go to `chrome://extensions/`
3. Click reload button on your extension
4. Test the changes

## 📞 Support

For issues:
- Check browser console for errors
- Review backend API logs
- Ensure all prerequisites are met
- Check GitHub issues for similar problems

---

Made with ❤️ by Anup
