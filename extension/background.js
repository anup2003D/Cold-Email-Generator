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
    if (request.action === 'jobPageDetected') {
        // Update extension badge when job page is detected
        chrome.action.setBadgeText({
            text: '✓',
            tabId: sender.tab.id
        });
        chrome.action.setBadgeBackgroundColor({
            color: '#4CAF50',
            tabId: sender.tab.id
        });
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

// Clear badge when tab is updated
chrome.tabs.onUpdated.addListener((tabId, changeInfo) => {
    if (changeInfo.status === 'complete') {
        chrome.action.setBadgeText({ text: '', tabId: tabId });
    }
});
