// Configuration
const API_BASE_URL = 'http://localhost:8000';

// State management
let currentJob = null;
let generatedEmail = null;
let emailSubject = null;
let hasResume = false;

// DOM Elements
const initialState = document.getElementById('initialState');
const jobExtractedState = document.getElementById('jobExtractedState');
const emailGeneratedState = document.getElementById('emailGeneratedState');
const loadingState = document.getElementById('loadingState');

const statusMessage = document.getElementById('statusMessage');
const loadingMessage = document.getElementById('loadingMessage');
const jobInfo = document.getElementById('jobInfo');
const emailPreview = document.getElementById('emailPreview');
const recipientEmail = document.getElementById('recipientEmail');

// Resume elements
const resumeStatus = document.getElementById('resumeStatus');
const resumeFileInput = document.getElementById('resumeFileInput');
const uploadResumeBtn = document.getElementById('uploadResumeBtn');
const changeResumeBtn = document.getElementById('changeResumeBtn');

// Buttons
const extractJobBtn = document.getElementById('extractJobBtn');
const generateEmailBtn = document.getElementById('generateEmailBtn');
const sendEmailBtn = document.getElementById('sendEmailBtn');
const editEmailBtn = document.getElementById('editEmailBtn');
const regenerateBtn = document.getElementById('regenerateBtn');

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await checkResumeStatus();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    extractJobBtn.addEventListener('click', extractJobFromPage);
    generateEmailBtn.addEventListener('click', generateEmail);
    sendEmailBtn.addEventListener('click', sendEmail);
    editEmailBtn.addEventListener('click', editEmail);
    regenerateBtn.addEventListener('click', () => {
        showState('jobExtracted');
    });

    // Resume event listeners
    uploadResumeBtn.addEventListener('click', () => resumeFileInput.click());
    changeResumeBtn.addEventListener('click', changeResume);
    resumeFileInput.addEventListener('change', handleResumeUpload);
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

// Extract job from current page
async function extractJobFromPage() {
    try {
        showLoading('Extracting job details...');

        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        const results = await chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                const keywords = ['job description', 'description', 'overview', 'responsibilities', 'requirements', 'qualifications', 'about the role', 'about this job'];

                let bestMatch = null;
                let maxLength = 0;

                const walker = document.createTreeWalker(
                    document.body,
                    NodeFilter.SHOW_TEXT,
                    null,
                    false
                );

                const potentialSections = new Set();

                while (walker.nextNode()) {
                    const text = walker.currentNode.textContent.toLowerCase();
                    if (keywords.some(kw => text.includes(kw))) {
                        let element = walker.currentNode.parentElement;
                        for (let i = 0; i < 3 && element.parentElement; i++) {
                            element = element.parentElement;
                        }
                        potentialSections.add(element);
                    }
                }

                for (const section of potentialSections) {
                    const text = section.innerText;
                    if (text && text.length > maxLength) {
                        maxLength = text.length;
                        bestMatch = text;
                    }
                }

                if (!bestMatch || maxLength < 200) {
                    const selectors = [
                        '[class*="job-description"]',
                        '[class*="job-details"]',
                        '[class*="description"]',
                        '[id*="job-description"]',
                        '[id*="description"]',
                        'article',
                        'main',
                        '.content'
                    ];

                    for (const selector of selectors) {
                        const element = document.querySelector(selector);
                        if (element && element.innerText.length > 200) {
                            bestMatch = element.innerText;
                            break;
                        }
                    }
                }

                if (!bestMatch || bestMatch.length < 100) {
                    bestMatch = document.body.innerText;
                }

                return bestMatch;
            }
        });

        const pageText = results[0].result;

        if (!pageText || pageText.length < 100) {
            throw new Error('Could not extract enough content from the page. Make sure you\'re on a job posting page.');
        }

        const response = await fetch(`${API_BASE_URL}/api/extract-job`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: pageText })
        });

        if (!response.ok) {
            throw new Error('Failed to extract job details');
        }

        const data = await response.json();
        currentJob = data.jobs[0];

        displayJobInfo(currentJob);
        showState('jobExtracted');

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

// Generate email
async function generateEmail() {
    try {
        showLoading('Generating personalized email...');

        const response = await fetch(`${API_BASE_URL}/api/generate-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_data: currentJob })
        });

        if (!response.ok) {
            throw new Error('Failed to generate email');
        }

        const data = await response.json();
        generatedEmail = data.email;
        emailSubject = data.subject;

        emailPreview.textContent = generatedEmail;

        const companyEmail = await guessCompanyEmail();
        if (companyEmail) {
            recipientEmail.value = companyEmail;
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

        showLoading('Sending email via SMTP...');

        const response = await fetch(`${API_BASE_URL}/api/send-email-smtp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                to_email: email,
                subject: emailSubject,
                body: generatedEmail
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

// Edit email
function editEmail() {
    const newEmail = prompt('Edit your email:', generatedEmail);
    if (newEmail !== null && newEmail.trim() !== '') {
        generatedEmail = newEmail;
        emailPreview.textContent = generatedEmail;
    }
}

// State management
function showState(state) {
    initialState.classList.add('hidden');
    jobExtractedState.classList.add('hidden');
    emailGeneratedState.classList.add('hidden');
    loadingState.classList.add('hidden');

    switch (state) {
        case 'initial':
            initialState.classList.remove('hidden');
            break;
        case 'jobExtracted':
            jobExtractedState.classList.remove('hidden');
            break;
        case 'emailGenerated':
            emailGeneratedState.classList.remove('hidden');
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
    generatedEmail = null;
    emailSubject = null;
    recipientEmail.value = '';
    statusMessage.className = 'status info';
    statusMessage.textContent = 'Ready to generate cold emails!';
    showState('initial');
}
