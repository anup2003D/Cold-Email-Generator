// Background service worker
// Handles background tasks and extension lifecycle

// Listen for extension installation
chrome.runtime.onInstalled.addListener(() => {
    console.log('Cold Email Generator Extension Installed');

    // Set default storage values
    chrome.storage.local.set({
        api_base_url: 'http://localhost:8000'
    });
});

// Listen for messages from content scripts and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'pageTypeDetected') {
        // Update extension badge based on detected page type
        const tabId = sender.tab.id;

        if (request.pageType === 'job_posting') {
            // 🟢 Green "JD" badge for job postings
            chrome.action.setBadgeText({ text: 'JD', tabId });
            chrome.action.setBadgeBackgroundColor({ color: '#4CAF50', tabId });
        } else if (request.pageType === 'company_website') {
            // 🔵 Blue "CO" badge for company websites
            chrome.action.setBadgeText({ text: 'CO', tabId });
            chrome.action.setBadgeBackgroundColor({ color: '#1976D2', tabId });
        } else {
            // No badge for generic pages
            chrome.action.setBadgeText({ text: '', tabId });
        }
    }

    if (request.action === 'apiRequest') {
        fetch(request.url, request.options)
            .then(response => response.json())
            .then(data => sendResponse({ success: true, data: data }))
            .catch(error => sendResponse({ success: false, error: error.message }));
        return true; // Keep channel open for async response
    }

    return true;
});

// Clear badge when tab navigates to a new page
chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
    if (changeInfo.status === 'loading') {
        chrome.action.setBadgeText({ text: '', tabId: tabId });
    }
});
