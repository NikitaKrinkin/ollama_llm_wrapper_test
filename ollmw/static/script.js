const chatContainer = document.getElementById('chatContainer');
let isPromptSet = chatContainer.getAttribute('data-prompt-set') === 'true';

function updateUI() {
    const input = document.getElementById('userInput');
    const defaultBtn = document.getElementById('defaultBtn');
    const sendBtn = document.getElementById('sendBtn');
    
    if (!isPromptSet) {
        input.placeholder = "Задайте роль модели (или выберите по умолчанию)...";
        sendBtn.textContent = "Задать роль";
        defaultBtn.style.display = "inline-block";
    } else {
        input.placeholder = "Введите сообщение...";
        sendBtn.textContent = "Отправить";
        defaultBtn.style.display = "none";
    }
}

function submitInput() {
    if (!isPromptSet) {
        sendPrompt(false);
    } else {
        sendMessage();
    }
}

async function sendPrompt(useDefault) {
    const input = document.getElementById('userInput');
    const text = input.value.trim();

    if (!useDefault && !text) return;

    setLoading(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                message: text,
                is_system_init: true,
                use_default: useDefault
            })
        });

        const data = await response.json();
        if (response.ok) {
            appendMessage('system_info', data.response);
            isPromptSet = true;
            input.value = '';
            updateUI();
        } else {
            appendMessage('error', data.error || 'Ошибка установки промпта.');
        }
    } catch (err) {
        appendMessage('error', 'Ошибка сети.');
    } finally {
        setLoading(false);
    }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const text = input.value.trim();

    if (!text) return;

    appendMessage('user', text);
    input.value = '';
    setLoading(true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        if (response.ok) {
            appendMessage('assistant', data.response);
        } else {
            appendMessage('error', data.error || 'Произошла ошибка при получении ответа.');
        }
    } catch (err) {
        appendMessage('error', 'Ошибка сети при обращении к серверу.');
    } finally {
        setLoading(false);
    }
}

async function clearChat() {
    await fetch('/api/clear', { method: 'POST' });
    document.getElementById('messages').innerHTML = '';
    isPromptSet = false;
    updateUI();
}

function appendMessage(role, text) {
    const messagesDiv = document.getElementById('messages');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    msgDiv.textContent = text;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function setLoading(isLoading) {
    document.getElementById('userInput').disabled = isLoading;
    document.getElementById('sendBtn').disabled = isLoading;
    document.getElementById('defaultBtn').disabled = isLoading;
    if (!isLoading) document.getElementById('userInput').focus();
}

// Initialization on load
updateUI();
