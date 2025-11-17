// Global variables
let isDarkMode = localStorage.getItem('darkMode') === 'true';
let isAnalyzing = false;

// DOM elements
const emailInput = document.getElementById('emailInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const themeToggle = document.getElementById('themeToggle');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const errorState = document.getElementById('errorState');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const copyResultsBtn = document.getElementById('copyResultsBtn');
const retryBtn = document.getElementById('retryBtn');

// Result elements
const resultIcon = document.getElementById('resultIcon');
const resultTitle = document.getElementById('resultTitle');
const resultSubtitle = document.getElementById('resultSubtitle');
const confidenceBadge = document.getElementById('confidenceBadge');
const confidenceValue = document.getElementById('confidenceValue');
const safeProgress = document.getElementById('safeProgress');
const phishingProgress = document.getElementById('phishingProgress');
const safePercent = document.getElementById('safePercent');
const phishingPercent = document.getElementById('phishingPercent');
const explanationContent = document.getElementById('explanationContent');
const errorMessage = document.getElementById('errorMessage');

// API configuration
const API_BASE_URL = window.location.origin + '/api';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize theme
    initializeTheme();
    
    // Add event listeners
    addEventListeners();
    
    // Check API health
    checkAPIHealth();
}

function initializeTheme() {
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon();
    }
}

function updateThemeIcon() {
    const icon = themeToggle.querySelector('i');
    if (isDarkMode) {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

function addEventListeners() {
    // Theme toggle
    themeToggle.addEventListener('click', toggleTheme);
    
    // Analyze button
    analyzeBtn.addEventListener('click', analyzeEmail);
    
    // Clear button
    clearBtn.addEventListener('click', clearInput);
    
    // New analysis button
    newAnalysisBtn.addEventListener('click', resetToInput);
    
    // Copy results button
    copyResultsBtn.addEventListener('click', copyResults);
    
    // Retry button
    retryBtn.addEventListener('click', analyzeEmail);
    
    // Enter key to analyze (Ctrl+Enter)
    emailInput.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            analyzeEmail();
        }
    });
    
    // Auto-resize textarea
    emailInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.max(120, this.scrollHeight) + 'px';
    });
}

function toggleTheme() {
    isDarkMode = !isDarkMode;
    localStorage.setItem('darkMode', isDarkMode);
    
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
    
    updateThemeIcon();
}

function clearInput() {
    emailInput.value = '';
    emailInput.style.height = '120px';
    emailInput.focus();
}

async function checkAPIHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (!data.model_loaded) {
            showError('API is running but model is not loaded. Please check the server.');
        }
    } catch (error) {
        showError('Unable to connect to the API. Please ensure the backend server is running on localhost:5000.');
    }
}

async function analyzeEmail() {
    if (isAnalyzing) return;
    
    const emailText = emailInput.value.trim();
    
    if (!emailText) {
        showError('Please enter an email to analyze.');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        isAnalyzing = true;
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        
        // Make API request
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email_text: emailText
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showResults(data);
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
        
    } catch (error) {
        console.error('Analysis error:', error);
        showError('An error occurred while analyzing the email. Please try again.');
    } finally {
        isAnalyzing = false;
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-search"></i> Analyze Email';
    }
}

function showLoading() {
    hideAllStates();
    loadingState.classList.remove('hidden');
}

function showResults(data) {
    hideAllStates();
    
    const { prediction, explanation } = data;
    
    // Update main result
    updateMainResult(prediction, explanation);
    
    // Update progress bars
    updateProgressBars(prediction);
    
    // Update explanation
    updateExplanation(explanation);
    
    // Show results
    resultsSection.classList.remove('hidden');
    
    // Smooth scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function updateMainResult(prediction, explanation) {
    const isPhishing = prediction.prediction === 'Phishing';
    
    // Update icon
    resultIcon.className = `result-icon ${isPhishing ? 'phishing' : 'safe'}`;
    resultIcon.innerHTML = `<i class="fas ${isPhishing ? 'fa-exclamation-triangle' : 'fa-shield-check'}"></i>`;
    
    // Update title and subtitle
    resultTitle.textContent = isPhishing ? 'Phishing Email Detected' : 'Safe Email';
    resultSubtitle.textContent = isPhishing ? 'This email appears to be a phishing attempt' : 'This email appears to be legitimate';
    
    // Update confidence
    confidenceValue.textContent = `${prediction.confidence.toFixed(1)}%`;
    
    // Update confidence badge color
    if (isPhishing) {
        confidenceBadge.style.backgroundColor = 'var(--danger-color)';
    } else {
        confidenceBadge.style.backgroundColor = 'var(--success-color)';
    }
}

function updateProgressBars(prediction) {
    const safeProb = prediction.safe_probability;
    const phishingProb = prediction.phishing_probability;
    
    // Animate progress bars
    setTimeout(() => {
        safeProgress.style.width = `${safeProb}%`;
        phishingProgress.style.width = `${phishingProb}%`;
    }, 100);
    
    // Update percentages
    safePercent.textContent = `${safeProb.toFixed(1)}%`;
    phishingPercent.textContent = `${phishingProb.toFixed(1)}%`;
}

function updateExplanation(explanation) {
    explanationContent.innerHTML = '';
    
    // Add reasoning
    if (explanation.reasoning && explanation.reasoning.length > 0) {
        const reasoningList = document.createElement('ul');
        reasoningList.className = 'explanation-list';
        
        explanation.reasoning.forEach(reason => {
            const listItem = document.createElement('li');
            listItem.textContent = reason;
            reasoningList.appendChild(listItem);
        });
        
        explanationContent.appendChild(reasoningList);
    }
    
    // Add indicators if available
    if (explanation.indicators && (explanation.indicators.phishing_indicators?.length || explanation.indicators.safe_indicators?.length)) {
        const indicatorsGrid = document.createElement('div');
        indicatorsGrid.className = 'indicators-grid';
        
        // Phishing indicators
        if (explanation.indicators.phishing_indicators?.length > 0) {
            const phishingGroup = document.createElement('div');
            phishingGroup.className = 'indicator-group phishing';
            phishingGroup.innerHTML = `
                <h5><i class="fas fa-exclamation-triangle"></i> Phishing Indicators</h5>
                <div class="indicator-tags">
                    ${explanation.indicators.phishing_indicators.map(indicator => 
                        `<span class="indicator-tag">${indicator}</span>`
                    ).join('')}
                </div>
            `;
            indicatorsGrid.appendChild(phishingGroup);
        }
        
        // Safe indicators
        if (explanation.indicators.safe_indicators?.length > 0) {
            const safeGroup = document.createElement('div');
            safeGroup.className = 'indicator-group safe';
            safeGroup.innerHTML = `
                <h5><i class="fas fa-check-circle"></i> Safe Indicators</h5>
                <div class="indicator-tags">
                    ${explanation.indicators.safe_indicators.map(indicator => 
                        `<span class="indicator-tag">${indicator}</span>`
                    ).join('')}
                </div>
            `;
            indicatorsGrid.appendChild(safeGroup);
        }
        
        explanationContent.appendChild(indicatorsGrid);
    }
}

function copyResults() {
    const emailText = emailInput.value;
    const result = resultsSection.querySelector('.result-card');
    const explanation = resultsSection.querySelector('.explanation-card');
    
    const textToCopy = `
Phishing Email Detection Results
================================

Email Text:
${emailText}

Analysis Results:
${result.textContent}

Explanation:
${explanation.textContent}
    `.trim();
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        // Show temporary success message
        const originalText = copyResultsBtn.innerHTML;
        copyResultsBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
        copyResultsBtn.style.backgroundColor = 'var(--success-color)';
        
        setTimeout(() => {
            copyResultsBtn.innerHTML = originalText;
            copyResultsBtn.style.backgroundColor = '';
        }, 2000);
    }).catch(() => {
        showError('Unable to copy results to clipboard.');
    });
}

function resetToInput() {
    hideAllStates();
    emailInput.focus();
}

function showError(message) {
    hideAllStates();
    errorMessage.textContent = message;
    errorState.classList.remove('hidden');
}

function hideAllStates() {
    loadingState.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorState.classList.add('hidden');
}

// Sample email templates for testing
const sampleEmails = {
    phishing: [
        "Congratulations! You have won $1000000! Click here to claim your prize immediately!",
        "URGENT: Your bank account will be suspended. Verify your identity now at this secure link!",
        "Limited time offer! Get a free iPhone 15! Click here and fill out the form!",
        "Dear user, we detected suspicious activity. Reset your password immediately to avoid account closure!"
    ],
    safe: [
        "Hi John, I hope you're doing well. Can we schedule a meeting for next week?",
        "Thank you for your purchase. Your order confirmation is attached.",
        "Team meeting scheduled for Friday at 2 PM in conference room B.",
        "Please review the attached document and provide your feedback by Monday."
    ]
};

// Add sample email functionality (can be expanded with UI)
function loadSampleEmail(type) {
    const samples = sampleEmails[type];
    if (samples && samples.length > 0) {
        const randomSample = samples[Math.floor(Math.random() * samples.length)];
        emailInput.value = randomSample;
        emailInput.style.height = 'auto';
        emailInput.style.height = emailInput.scrollHeight + 'px';
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Alt + 1: Load phishing sample
    if (e.altKey && e.key === '1') {
        e.preventDefault();
        loadSampleEmail('phishing');
    }
    
    // Alt + 2: Load safe sample
    if (e.altKey && e.key === '2') {
        e.preventDefault();
        loadSampleEmail('safe');
    }
    
    // Escape: Clear input
    if (e.key === 'Escape') {
        clearInput();
    }
});

// Performance monitoring
function logPerformance(action, duration) {
    console.log(`Performance: ${action} took ${duration}ms`);
}

// Error handling for unhandled promises
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    showError('An unexpected error occurred. Please refresh the page and try again.');
});

// Add CSS for loading animation enhancement
const style = document.createElement('style');
style.textContent = `
    .btn-primary:disabled {
        background-color: var(--text-muted) !important;
        transform: none !important;
    }
    
    .spinner {
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);