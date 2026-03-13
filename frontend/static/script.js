// ======================================
// Policy Assistant - JavaScript Functions
// ======================================

// API Configuration
const API_BASE = 'http://localhost:5000/api';
let currentVoiceFilePath = null;

// ======================================
// Section Navigation
// ======================================

function switchSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
    }

    // Update nav buttons
    const navBtns = document.querySelectorAll('.nav-btn');
    navBtns.forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-section') === sectionId) {
            btn.classList.add('active');
        }
    });

    // Scroll to top
    window.scrollTo(0, 0);
}

// Navigation button event listeners
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const sectionId = e.target.getAttribute('data-section');
        switchSection(sectionId);
        
        // Load workflow data when navigating to workflow tab
        if (sectionId === 'workflow') {
            loadWorkflow();
        }
    });
});

// ======================================
// Policy Document Functions
// ======================================

function openPolicyInNewTab() {
    window.open('/policy', '_blank');
}

function downloadPolicyPDF() {
    // Open the policy page in a new tab and trigger print dialog for PDF save
    const printWindow = window.open('/policy', '_blank');
    
    // Wait for the page to load, then trigger print
    if (printWindow) {
        printWindow.onload = function() {
            setTimeout(() => {
                printWindow.print();
            }, 500);
        };
    }
    
    showMessage('Opening print dialog - select "Save as PDF" to download', 'info');
}

function getSummary() {
    const container = document.getElementById('policy-summary-container');
    const summaryDiv = document.getElementById('policy-summary');

    container.style.display = 'block';
    summaryDiv.innerHTML = '<span class="loading"></span> Generating summary...';

    fetch(`${API_BASE}/summary`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to get summary');
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Format the summary as clean paragraphs
                const summaryText = data.summary;
                const formattedSummary = summaryText
                    .split('\n')
                    .filter(line => line.trim())
                    .map(line => `<p>${line}</p>`)
                    .join('');
                summaryDiv.innerHTML = formattedSummary;
            } else {
                summaryDiv.innerHTML = `<p style="color: red;">Error: ${data.summary}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            summaryDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
}

// ======================================
// AI Assistant Functions
// ======================================

function askQuestion() {
    const questionInput = document.getElementById('policy-question');
    const question = questionInput.value.trim();

    if (!question) {
        showMessage('Please enter a question', 'error');
        return;
    }

    askAbout(question);
    questionInput.value = '';
}

function handleQuestionKeypress(event) {
    if (event.key === 'Enter') {
        askQuestion();
    }
}

function askAbout(question) {
    const statusMsg = document.getElementById('status-message');
    const answerContainer = document.getElementById('answer-container');

    // Show loading state
    statusMsg.innerHTML = '<span class="loading"></span> Getting answer...';
    statusMsg.style.display = 'block';
    answerContainer.style.display = 'none';

    // Send question to backend
    fetch(`${API_BASE}/explain`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question })
    })
        .then(response => {
            if (!response.ok) throw new Error('Failed to get explanation');
            return response.json();
        })
        .then(data => {
            statusMsg.style.display = 'none';

            if (data.success) {
                displayAnswer(data.explanation);
            } else {
                showMessage(`Error: ${data.explanation}`, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage(`Error: ${error.message}`, 'error');
            statusMsg.style.display = 'none';
        });
}

function displayAnswer(explanation) {
    const container = document.getElementById('answer-container');
    const textDiv = document.getElementById('answer-text');

    textDiv.innerHTML = explanation
        .split('\n')
        .filter(line => line.trim())
        .map(line => `<p>${line}</p>`)
        .join('');

    container.style.display = 'block';

    // Reset voice section
    resetVoiceSection();
}

function closeAnswer() {
    document.getElementById('answer-container').style.display = 'none';
}

// ======================================
// Voice Synthesis Functions
// ======================================

async function pollVoiceStatus(taskId, maxAttempts = 30) {
    for (let i = 0; i < maxAttempts; i++) {
        await new Promise(resolve => setTimeout(resolve, 500));
        
        try {
            const response = await fetch(`${API_BASE}/voice-status/${taskId}`);
            const data = await response.json();
            
            if (data.status === 'processing') {
                continue; // Keep polling
            }
            
            return data; // Return completed result
        } catch (err) {
            console.error('[Voice Poll] Error:', err);
        }
    }
    
    return { success: false, message: 'Voice generation timed out' };
}

async function generateVoiceNote() {
    const answerText = document.getElementById('answer-text').textContent;
    const language = document.getElementById('language-select').value;
    const statusDiv = document.getElementById('voice-status');
    const playerDiv = document.getElementById('voice-player');

    if (!answerText) {
        showMessage('Please get an answer first', 'error');
        return;
    }

    // Show loading
    statusDiv.style.display = 'block';
    statusDiv.innerHTML = '<span class="loading"></span> Generating voice note...';
    playerDiv.style.display = 'none';

    try {
        console.log('[Voice] Sending request for language:', language);
        console.log('[Voice] Text length:', answerText.length);
        
        const response = await fetch(`${API_BASE}/voice`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: answerText,
                language: language
            })
        });

        console.log('[Voice] Response status:', response.status);
        
        const data = await response.json();
        console.log('[Voice] Response data:', data);

        if (data.success && data.task_id) {
            // Poll for completion
            statusDiv.innerHTML = '<span class="loading"></span> Creating voice note...';
            
            const result = await pollVoiceStatus(data.task_id);
            
            if (result.success && result.filename) {
                statusDiv.innerHTML = `✓ Voice note created successfully!`;
                statusDiv.style.borderLeftColor = '#10b981';
                
                // Set up audio player
                currentVoiceFilePath = result.file_path;
                const audioElement = document.getElementById('voice-audio');
                const audioSrc = `/voice/${result.filename}`;
                
                console.log('[Voice] Audio src:', audioSrc);
                
                audioElement.src = audioSrc;
                audioElement.load();
                playerDiv.style.display = 'block';

                // Try to play
                audioElement.play()
                    .then(() => {
                        console.log('[Voice] Auto-play successful');
                        statusDiv.innerHTML += '<br/>Playing audio...';
                    })
                    .catch(err => {
                        console.log('[Voice] Auto-play prevented (likely browser policy):', err);
                        statusDiv.innerHTML += '<br/>Click play button to listen';
                    });
            } else {
                const errorMsg = result.message || 'Voice generation failed';
                statusDiv.innerHTML = `✗ Error: ${errorMsg}`;
                statusDiv.style.borderLeftColor = '#ef4444';
            }
        } else if (data.success && data.filename) {
            // Backward compatibility - direct response
            statusDiv.innerHTML = `✓ Voice note created successfully!`;
            statusDiv.style.borderLeftColor = '#10b981';
            
            currentVoiceFilePath = data.file_path;
            const audioElement = document.getElementById('voice-audio');
            const audioSrc = `/voice/${data.filename}`;
            
            audioElement.src = audioSrc;
            audioElement.load();
            playerDiv.style.display = 'block';
            
            audioElement.play()
                .then(() => {
                    statusDiv.innerHTML += '<br/>Playing audio...';
                })
                .catch(err => {
                    statusDiv.innerHTML += '<br/>Click play button to listen';
                });
        } else {
            const errorMsg = data.message || 'Unknown error';
            statusDiv.innerHTML = `✗ Error: ${errorMsg}`;
            statusDiv.style.borderLeftColor = '#ef4444';
            console.error('[Voice] Generation failed:', data);
        }
    } catch (error) {
        console.error('[Voice] Fetch error:', error);
        statusDiv.innerHTML = `✗ Error: ${error.message}`;
        statusDiv.style.borderLeftColor = '#ef4444';
    }
}

function downloadVoiceNote() {
    if (!currentVoiceFilePath) {
        showMessage('No voice file available', 'error');
        return;
    }

    const filename = currentVoiceFilePath.split('\\').pop() || 'policy_voice.mp3';
    const link = document.createElement('a');
    link.href = `/voice/${filename}`;
    link.download = filename;
    link.click();
}

function resetVoiceSection() {
    document.getElementById('voice-status').style.display = 'none';
    document.getElementById('voice-player').style.display = 'none';
    currentVoiceFilePath = null;
}

// ======================================
// Workflow Functions
// ======================================

function loadWorkflow() {
    switchSection('workflow');
    
    const container = document.getElementById('workflow-steps');
    
    // Check if workflow is already loaded
    if (container && container.innerHTML && container.innerHTML.includes('workflow-step')) {
        return; // Already loaded
    }
    
    container.innerHTML = '<span class="loading"></span> Loading workflow...';

    fetch(`${API_BASE}/request-flow`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to load workflow');
            return response.json();
        })
        .then(data => {
            displayWorkflow(data);
        })
        .catch(error => {
            console.error('Error:', error);
            container.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
}

function displayWorkflow(data) {
    const container = document.getElementById('workflow-steps');
    container.innerHTML = '';

    data.steps.forEach(step => {
        const stepDiv = document.createElement('div');
        stepDiv.className = 'workflow-step';
        stepDiv.innerHTML = `
            <div class="step-number">${step.step}</div>
            <h4>${step.name}</h4>
            <p>${step.description}</p>
            <div class="step-duration">⏱️ ${step.duration}</div>
        `;
        container.appendChild(stepDiv);
    });

    // Add approval criteria section
    const criteriaDiv = document.createElement('div');
    criteriaDiv.className = 'workflow-step';
    criteriaDiv.style.gridColumn = '1 / -1';
    criteriaDiv.innerHTML = `
        <h4>✓ Approval Criteria</h4>
        <ul>
            ${data.approval_criteria.map(criterion => `<li>${criterion}</li>`).join('')}
        </ul>
    `;
    container.appendChild(criteriaDiv);
}

// ======================================
// Utility Functions
// ======================================

function showMessage(message, type = 'info') {
    const statusMsg = document.getElementById('status-message');
    statusMsg.textContent = message;
    statusMsg.className = `status-message ${type}`;
    statusMsg.style.display = 'block';

    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusMsg.style.display = 'none';
    }, 5000);
}

// ======================================
// Initialization
// ======================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Policy Assistant loaded successfully');
    
    // Check policy status
    fetch(`${API_BASE}/policy-status`)
        .then(response => response.json())
        .then(data => {
            if (data.loaded) {
                console.log('✓ Policy document loaded');
            } else {
                console.warn('⚠ Policy document not loaded');
            }
        })
        .catch(error => console.error('Error checking policy status:', error));

    // Load languages on initialization
    loadLanguages();
});

function loadLanguages() {
    fetch(`${API_BASE}/languages`)
        .then(response => response.json())
        .then(data => {
            console.log('Available languages:', data.count);
        })
        .catch(error => console.error('Error loading languages:', error));
}

// ======================================
// Export Functions for HTML onclick
// ======================================

window.switchSection = switchSection;
window.openPolicyInNewTab = openPolicyInNewTab;
window.downloadPolicyPDF = downloadPolicyPDF;
window.getSummary = getSummary;
window.askQuestion = askQuestion;
window.handleQuestionKeypress = handleQuestionKeypress;
window.askAbout = askAbout;
window.generateVoiceNote = generateVoiceNote;
window.downloadVoiceNote = downloadVoiceNote;
window.closeAnswer = closeAnswer;
window.loadWorkflow = loadWorkflow;
