// AI Chatbot Interface JavaScript

document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatContainer = document.getElementById('chat-messages');

    if (!chatForm) return;

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const userMsg = chatInput.value.trim();
        if (!userMsg) return;

        // Render User Message
        appendMessage('user', userMsg);
        chatInput.value = '';

        // Show typing indicator
        const typingId = appendTypingIndicator();

        // Send API request
        fetch('/user/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMsg })
        })
        .then(res => res.json())
        .then(data => {
            removeTypingIndicator(typingId);
            appendMessage('bot', data.response);
        })
        .catch(err => {
            removeTypingIndicator(typingId);
            appendMessage('bot', "I'm having trouble connecting to the network right now. Please try again.");
        });
    });

    function appendMessage(sender, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `chat-bubble ${sender}-bubble`;
        
        const avatar = sender === 'user' 
            ? '<div class="chat-avatar user-avatar"><i class="bi bi-person-fill"></i></div>' 
            : '<div class="chat-avatar bot-avatar"><i class="bi bi-robot"></i></div>';
            
        msgDiv.innerHTML = `${avatar}<div class="bubble-content"><p>${text.replace(/\n/g, '<br>')}</p></div>`;
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function appendTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.id = id;
        msgDiv.className = 'chat-bubble bot-bubble typing-bubble';
        msgDiv.innerHTML = `<div class="chat-avatar bot-avatar"><i class="bi bi-robot"></i></div><div class="bubble-content"><span class="typing-dots"><span>.</span><span>.</span><span>.</span></span></div>`;
        chatContainer.appendChild(msgDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        return id;
    }

    function removeTypingIndicator(id) {
        const elem = document.getElementById(id);
        if (elem) elem.remove();
    }
});
