// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State management
let currentJob = null;
let currentCompanyData = null;
let currentPageType = 'job_posting'; // 'job_posting', 'company_website', or 'generic'
let generatedEmail = null;
let emailSubject = null;
let hasResume = false;
let attachResume = true;

// DOM Elements
const initialState = document.getElementById('initialState');
const jobExtractedState = document.getElementById('jobExtractedState');
const companyDetectedState = document.getElementById('companyDetectedState');
const genericState = document.getElementById('genericState');
const emailGeneratedState = document.getElementById('emailGeneratedState');
const loadingState = document.getElementById('loadingState');

const statusMessage = document.getElementById('statusMessage');
const loadingMessage = document.getElementById('loadingMessage');
const jobInfo = document.getElementById('jobInfo');
const companyInfo = document.getElementById('companyInfo');
const emailPreview = document.getElementById('emailPreview');
const recipientEmail = document.getElementById('recipientEmail');
const contextBanner = document.getElementById('contextBanner');
const attachResumeCheckbox = document.getElementById('attachResumeCheckbox');

// Resume elements
const resumeStatus = document.getElementById('resumeStatus');
const resumeFileInput = document.getElementById('resumeFileInput');
const uploadResumeBtn = document.getElementById('uploadResumeBtn');
const changeResumeBtn = document.getElementById('changeResumeBtn');

// Buttons
const extractJobBtn = document.getElementById('extractJobBtn');
const generateEmailBtn = document.getElementById('generateEmailBtn');
const generateCompanyEmailBtn = document.getElementById('generateCompanyEmailBtn');
const generateGenericEmailBtn = document.getElementById('generateGenericEmailBtn');
const sendEmailBtn = document.getElementById('sendEmailBtn');
const regenerateBtn = document.getElementById('regenerateBtn');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await checkResumeStatus();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    extractJobBtn.addEventListener('click', analyzeCurrentPage);
    generateEmailBtn.addEventListener('click', generateEmail);
    generateCompanyEmailBtn.addEventListener('click', generateEmail);
    generateGenericEmailBtn.addEventListener('click', generateEmail);
    sendEmailBtn.addEventListener('click', sendEmail);
    regenerateBtn.addEventListener('click', () => {
        if (currentPageType === 'job_posting') {
            showState('jobExtracted');
        } else if (currentPageType === 'company_website') {
            showState('companyDetected');
        } else {
            showState('generic');
        }
    });

    // Resume event listeners
    uploadResumeBtn.addEventListener('click', () => resumeFileInput.click());
    changeResumeBtn.addEventListener('click', changeResume);
    resumeFileInput.addEventListener('change', handleResumeUpload);

    // Attach resume checkbox listener
    if (attachResumeCheckbox) {
        attachResumeCheckbox.addEventListener('change', (e) => {
            attachResume = e.target.checked;
        });
    }
}

// Check Resume Status
async function checkResumeStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/resume-status`);
        const data = await response.json();

        if (data.success && data.has_resume) {
            hasResume = true;
            resumeStatus.innerHTML = `
                ✅ <strong>${data.applicant_name}</strong><br>
                <span style="font-size: 11px; opacity: 0.8;">${data.email || 'Resume uploaded'}</span>
            `;
            uploadResumeBtn.classList.add('hidden');
            changeResumeBtn.classList.remove('hidden');
        } else {
            hasResume = false;
            resumeStatus.textContent = '❌ No resume uploaded. Upload your resume for personalized emails.';
            uploadResumeBtn.classList.remove('hidden');
            changeResumeBtn.classList.add('hidden');
        }
    } catch (error) {
        console.error('Error checking resume status:', error);
        resumeStatus.textContent = '⚠️ Could not check resume status. Make sure the server is running.';
    }
}

// Handle Resume Upload
async function handleResumeUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.pdf')) {
        alert('Please upload a PDF file');
        return;
    }

    const applicantName = prompt('Enter your full name:', 'Your Name');
    if (!applicantName || applicantName.trim() === '') {
        alert('Name is required');
        resumeFileInput.value = '';
        return;
    }

    try {
        showLoading('Processing resume...');

        const formData = new FormData();
        formData.append('file', file);
        formData.append('applicant_name', applicantName.trim());

        const response = await fetch(`${API_BASE_URL}/api/upload-resume`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to upload resume');
        }

        const data = await response.json();

        if (data.success) {
            alert(`✅ Resume uploaded successfully!\n\nYour profile has been updated for: ${data.applicant_name}`);
            await checkResumeStatus();
            showState('initial');
        } else {
            throw new Error('Upload failed');
        }

    } catch (error) {
        showError(`Error uploading resume: ${error.message}`);
    } finally {
        resumeFileInput.value = '';
    }
}

// Change Resume
async function changeResume() {
    const confirmed = confirm('This will delete your current resume. Upload a new one?');
    if (!confirmed) return;

    try {
        showLoading('Removing current resume...');

        const response = await fetch(`${API_BASE_URL}/api/resume`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            alert('✅ Resume removed. You can now upload a new one.');
            await checkResumeStatus();
            resumeFileInput.click();
        } else {
            throw new Error('Failed to delete resume');
        }

        showState('initial');
    } catch (error) {
        showError(`Error changing resume: ${error.message}`);
    }
}

// Analyze current page using content script
async function analyzeCurrentPage() {
    try {
        showLoading('Analyzing page...');

        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        
        // Ask content script for page type and extracted content
        const response = await chrome.tabs.sendMessage(tab.id, { action: 'analyzePageType' });
        
        if (!response || !response.success) {
            throw new Error(response ? response.error : 'Failed to communicate with page. Try reloading the tab.');
        }

        currentPageType = response.pageType;
        const pageText = response.content;

        // Route based on page type
        if (currentPageType === 'job_posting') {
            showLoading('Extracting job details...');
            
            const apiResponse = await fetch(`${API_BASE_URL}/api/extract-job`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: pageText })
            });

            if (!apiResponse.ok) throw new Error('Failed to extract job details');
            
            const data = await apiResponse.json();
            currentJob = data.jobs[0];
            
            displayJobInfo(currentJob);
            showState('jobExtracted');
            
        } else if (currentPageType === 'company_website') {
            showLoading('Extracting company details...');
            
            const apiResponse = await fetch(`${API_BASE_URL}/api/extract-company`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: pageText })
            });

            if (!apiResponse.ok) throw new Error('Failed to extract company details');
            
            const data = await apiResponse.json();
            currentCompanyData = data.company_data;
            
            displayCompanyInfo(currentCompanyData);
            showState('companyDetected');
            
        } else {
            // Generic mode - no extraction needed
            showState('generic');
        }

    } catch (error) {
        showError(error.message);
    }
}

// Display job information
function displayJobInfo(job) {
    jobInfo.innerHTML = `
        <div class="job-info-item"><strong>Role:</strong> ${job.role || 'Not specified'}</div>
        <div class="job-info-item"><strong>Company:</strong> ${job.company_name || 'Not specified'}</div>
        <div class="job-info-item"><strong>Experience:</strong> ${job.experience || 'Not specified'}</div>
        <div class="job-info-item"><strong>Skills:</strong> ${job.skills || 'Not specified'}</div>
    `;
}

// Display company information
function displayCompanyInfo(company) {
    companyInfo.innerHTML = `
        <div class="job-info-item"><strong>Company:</strong> ${company.company_name || 'Not specified'}</div>
        <div class="job-info-item"><strong>Domain:</strong> ${company.company_domain || 'Not specified'}</div>
        <div class="job-info-item"><strong>Highlight:</strong> ${company.company_highlight || 'Not specified'}</div>
    `;
}

// Generate email based on current page type
async function generateEmail() {
    try {
        showLoading('Generating personalized email...');

        const requestBody = { page_type: currentPageType };
        if (currentPageType === 'job_posting') {
            requestBody.job_data = currentJob;
        } else if (currentPageType === 'company_website') {
            requestBody.company_data = currentCompanyData;
        }

        const response = await fetch(`${API_BASE_URL}/api/generate-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            throw new Error('Failed to generate email');
        }

        const data = await response.json();
        generatedEmail = data.email;
        emailSubject = data.subject;

        emailPreview.value = generatedEmail;

        const companyEmail = await guessCompanyEmail();
        if (companyEmail) {
            recipientEmail.value = companyEmail;
        } else {
            recipientEmail.value = '';
        }

        showState('emailGenerated');

    } catch (error) {
        showError(error.message);
    }
}

// Guess company email from page
async function guessCompanyEmail() {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
                const emails = document.body.innerText.match(emailRegex);
                return emails ? emails[0] : null;
            }
        });
        return results[0].result;
    } catch (error) {
        return null;
    }
}

// Send email via SMTP
async function sendEmail() {
    try {
        const email = recipientEmail.value.trim();
        if (!email) {
            throw new Error('Please enter recipient email');
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            throw new Error('Please enter a valid email address');
        }
        
        // Read the currently edited email from the textarea
        const currentEmailBody = emailPreview.value;
        if (!currentEmailBody || currentEmailBody.trim() === '') {
            throw new Error('Email body is empty');
        }

        showLoading('Sending email via SMTP...');

        const response = await fetch(`${API_BASE_URL}/api/send-email-smtp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                to_email: email,
                subject: emailSubject,
                body: currentEmailBody,
                attach_resume: attachResume
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to send email');
        }

        await response.json();
        showSuccess('Email sent successfully via SMTP! 🎉');

        setTimeout(() => {
            resetExtension();
        }, 2000);

    } catch (error) {
        showError(error.message);
    }
}

// State management
function showState(state) {
    initialState.classList.add('hidden');
    jobExtractedState.classList.add('hidden');
    companyDetectedState.classList.add('hidden');
    genericState.classList.add('hidden');
    emailGeneratedState.classList.add('hidden');
    loadingState.classList.add('hidden');
    
    // Reset banner display
    contextBanner.style.display = 'none';
    contextBanner.className = 'context-banner';

    switch (state) {
        case 'initial':
            initialState.classList.remove('hidden');
            break;
        case 'jobExtracted':
            jobExtractedState.classList.remove('hidden');
            contextBanner.style.display = 'block';
            contextBanner.classList.add('job');
            contextBanner.textContent = '💼 Job Posting Detected';
            break;
        case 'companyDetected':
            companyDetectedState.classList.remove('hidden');
            contextBanner.style.display = 'block';
            contextBanner.classList.add('company');
            contextBanner.textContent = '🏢 Company Website Detected';
            break;
        case 'generic':
            genericState.classList.remove('hidden');
            contextBanner.style.display = 'block';
            contextBanner.classList.add('generic');
            contextBanner.textContent = '📧 Generic Page — Resume-Only Email';
            break;
        case 'emailGenerated':
            emailGeneratedState.classList.remove('hidden');
            // Keep the banner showing for the email generated state
            contextBanner.style.display = 'block';
            if (currentPageType === 'job_posting') {
                contextBanner.classList.add('job');
                contextBanner.textContent = '💼 Job Posting Detected';
            } else if (currentPageType === 'company_website') {
                contextBanner.classList.add('company');
                contextBanner.textContent = '🏢 Company Website Detected';
            } else {
                contextBanner.classList.add('generic');
                contextBanner.textContent = '📧 Generic Page — Resume-Only Email';
            }
            break;
        case 'loading':
            loadingState.classList.remove('hidden');
            break;
    }
}

function showLoading(message) {
    loadingMessage.textContent = message;
    showState('loading');
}

function showError(message) {
    statusMessage.className = 'status error';
    statusMessage.textContent = '❌ ' + message;
    showState('initial');
}

function showSuccess(message) {
    statusMessage.className = 'status success';
    statusMessage.textContent = message;
    showState('initial');
}

function resetExtension() {
    currentJob = null;
    currentCompanyData = null;
    currentPageType = 'job_posting';
    generatedEmail = null;
    emailSubject = null;
    recipientEmail.value = '';
    statusMessage.className = 'status info';
    statusMessage.textContent = 'Ready to generate cold emails!';
    showState('initial');
}
