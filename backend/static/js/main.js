/* Main JS for CareerScope */

const API_BASE = "http://127.0.0.1:5000/api";

function toggleChat() {
    const chatWindow = document.getElementById('chatbot');
    chatWindow.classList.toggle('active');
}

async function handleChatInput(event) {
    if (event.key === 'Enter') {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        if (message) {
            addMessage(message, 'user');
            input.value = '';

            // Call Backend API
            try {
                const response = await fetch(`${API_BASE}/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });
                const data = await response.json();
                addMessage(data.reply, 'bot');
            } catch (error) {
                console.error('Error:', error);
                addMessage("Sorry, I can't connect to the server right now.", 'bot');
            }
        }
    }
}

function addMessage(text, sender) {
    const chatBody = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');

    msgDiv.style.borderRadius = "12px";
    msgDiv.style.padding = "0.5rem 1rem";
    msgDiv.style.marginBottom = "0.5rem";
    msgDiv.style.maxWidth = "80%";
    msgDiv.style.animation = "fadeIn 0.3s";

    if (sender === 'user') {
        msgDiv.style.background = "var(--primary)";
        msgDiv.style.color = "white";
        msgDiv.style.marginLeft = "auto";
    } else {
        msgDiv.style.background = "#eef2ff";
        msgDiv.style.color = "var(--text)";
    }

    msgDiv.innerText = text;
    chatBody.appendChild(msgDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
}

// Function to fetch colleges (for colleges.html)
async function fetchColleges() {
    try {
        const response = await fetch(`${API_BASE}/colleges`);
        const data = await response.json();
        // Here you would render the colleges list dynamically
        console.log("Loaded colleges:", data.colleges);
    } catch (e) {
        console.error("Failed to fetch colleges", e);
    }
}

// Simple Auth Check (Mock)
document.addEventListener('DOMContentLoaded', () => {
    const isLoggedIn = localStorage.getItem('userData');
    if (isLoggedIn) {
        // Change nav to show Dashboard instead of Login
        const navLinks = document.querySelector('.nav-links');
        if (navLinks) {
            // This is a simple mock replacement for demo purposes
            // In real app, render based on auth state
        }
    }

    // Check if on colleges page
    if (window.location.pathname.includes('colleges.html')) {
        fetchColleges();
    }
});
