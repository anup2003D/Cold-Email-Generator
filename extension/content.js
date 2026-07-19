// Content script - runs on web pages
// This script can access the DOM of the current page

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'extractContent') {
        // Backwards compatibility
        try {
            const content = extractPageContent(detectPageType());
            sendResponse({ success: true, content: content });
        } catch (error) {
            sendResponse({ success: false, error: error.message });
        }
    } else if (request.action === 'analyzePageType') {
        try {
            const pageType = detectPageType();
            const content = extractPageContent(pageType);
            sendResponse({ success: true, pageType: pageType, content: content });
        } catch (error) {
            sendResponse({ success: false, error: error.message });
        }
    }
    return true; // Keep the message channel open for async response
});

// Detect page type: job_posting, company_website, or generic
function detectPageType() {
    const url = window.location.href.toLowerCase();
    const bodyText = document.body.innerText.toLowerCase();
    
    // 1. Job Posting Detection
    let jobSignals = 0;
    const jobUrlKeywords = ['/jobs/', '/careers/', '/position/', '/opening/', '/apply/'];
    if (jobUrlKeywords.some(keyword => url.includes(keyword))) jobSignals++;
    
    const jobBoards = ['linkedin.com/jobs', 'indeed.com', 'glassdoor.com', 'naukri.com', 'greenhouse.io', 'lever.co'];
    if (jobBoards.some(board => url.includes(board))) jobSignals++;
    
    const jobContentIndicators = ['responsibilities', 'qualifications', 'requirements', 'apply now', 'experience required'];
    let contentMatches = 0;
    jobContentIndicators.forEach(indicator => {
        if (bodyText.includes(indicator)) contentMatches++;
    });
    if (contentMatches >= 2) jobSignals++;
    if (document.querySelector('[class*="job-description"]') !== null) jobSignals++;
    
    if (jobSignals >= 2) return 'job_posting';
    
    // 2. Company Website Detection
    let companySignals = 0;
    const nonCompanyDomains = ['google.com', 'bing.com', 'facebook.com', 'twitter.com', 'instagram.com', 'linkedin.com', 'youtube.com', 'github.com'];
    const isNonCompany = nonCompanyDomains.some(domain => url.includes(domain));
    
    if (!isNonCompany) {
        const companyIndicators = ['about us', 'our products', 'our services', 'contact us', 'founded in'];
        let companyMatches = 0;
        companyIndicators.forEach(indicator => {
            if (bodyText.includes(indicator)) companyMatches++;
        });
        if (companyMatches >= 1) companySignals++;
        
        // If it looks like a corporate site and has substantial text
        if (document.body.innerText.length >= 500 && companySignals > 0) {
            return 'company_website';
        }
    }
    
    // 3. Generic Fallback
    return 'generic';
}

// Extract content based on page type
function extractPageContent(pageType) {
    let text = '';
    
    if (pageType === 'job_posting') {
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
        
        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element && element.innerText.length > 200) {
                text = element.innerText;
                break;
            }
        }
    } else if (pageType === 'company_website') {
        // Extract from about, main, etc.
        const selectors = ['main', 'article', '.about', '#about', '.content'];
        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element && element.innerText.length > 200) {
                text = element.innerText;
                break;
            }
        }
    }
    
    // Fallback to body if nothing substantial found or generic
    if (!text || text.length < 200) {
        if (pageType === 'generic') {
            text = document.body.innerText.substring(0, 1000); // limit generic text
        } else {
            text = document.body.innerText;
        }
    }
    
    return text;
}

// Notify background script about page type
const detectedPageType = detectPageType();
chrome.runtime.sendMessage({ 
    action: 'pageTypeDetected',
    pageType: detectedPageType,
    url: window.location.href 
});
