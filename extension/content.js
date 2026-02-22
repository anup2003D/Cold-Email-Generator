// Content script - runs on web pages
// This script can access the DOM of the current page

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'extractContent') {
        try {
            const content = extractJobContent();
            sendResponse({ success: true, content: content });
        } catch (error) {
            sendResponse({ success: false, error: error.message });
        }
    }
    return true; // Keep the message channel open for async response
});

// Extract job content from page
function extractJobContent() {
    // Common job posting selectors
    const selectors = [
        '[class*="job-description"]',
        '[class*="job-details"]',
        '[class*="description"]',
        '[id*="job-description"]',
        '[data-testid*="job-description"]',
        'article',
        'main',
        '.content',
        '#content'
    ];
    
    let text = '';
    
    // Try each selector
    for (const selector of selectors) {
        const element = document.querySelector(selector);
        if (element && element.innerText.length > 200) {
            text = element.innerText;
            break;
        }
    }
    
    // Fallback to body if nothing substantial found
    if (!text || text.length < 200) {
        text = document.body.innerText;
    }
    
    return text;
}

// Detect if current page is a job posting
function isJobPostingPage() {
    const url = window.location.href.toLowerCase();
    const jobKeywords = ['job', 'career', 'position', 'opening', 'vacancy', 'hiring'];
    
    // Check URL
    const hasJobInUrl = jobKeywords.some(keyword => url.includes(keyword));
    
    // Check page title
    const title = document.title.toLowerCase();
    const hasJobInTitle = jobKeywords.some(keyword => title.includes(keyword));
    
    // Check for common job posting indicators
    const hasJobDescription = document.querySelector('[class*="job-description"]') !== null;
    
    return hasJobInUrl || hasJobInTitle || hasJobDescription;
}

// Notify background script if this is a job posting
if (isJobPostingPage()) {
    chrome.runtime.sendMessage({ 
        action: 'jobPageDetected',
        url: window.location.href 
    });
}
