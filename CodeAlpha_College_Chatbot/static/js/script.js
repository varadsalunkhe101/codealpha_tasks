const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");

// Send Message Function
function sendMessage() {

    const message = userInput.value.trim();

    if (message === "") return;

    // User Message
    chatBox.innerHTML += `
        <div class="message user-message">
            <div class="message-content">
                ${message}
            </div>
        </div>
    `;

    // Auto Scroll
    chatBox.scrollTop = chatBox.scrollHeight;

    // Clear Input
    userInput.value = "";

    // Typing Indicator
    const typingDiv = document.createElement("div");

    typingDiv.className = "message bot-message";
    typingDiv.id = "typingIndicator";

    typingDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    chatBox.appendChild(typingDiv);

    chatBox.scrollTop = chatBox.scrollHeight;

    // Send to Flask
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message
        })
    })
    .then(response => response.json())
    .then(data => {

        // Remove typing indicator
        document.getElementById("typingIndicator")?.remove();

        // Bot response
        chatBox.innerHTML += `
            <div class="message bot-message">
                <div class="message-content">
                    <i class="bi bi-robot me-2"></i>
                    ${data.response}
                </div>
            </div>
        `;

        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {

        document.getElementById("typingIndicator")?.remove();

        chatBox.innerHTML += `
            <div class="message bot-message">
                <div class="message-content">
                    <i class="bi bi-exclamation-triangle me-2"></i>
                    Something went wrong. Please try again.
                </div>
            </div>
        `;

        console.error(error);
    });
}

// Send Button Click
sendBtn.addEventListener("click", sendMessage);

// Enter Key Support
userInput.addEventListener("keypress", function(event) {

    if (event.key === "Enter") {
        sendMessage();
    }

});

// Quick Action Buttons
document.querySelectorAll(".quick-btn").forEach(button => {

    button.addEventListener("click", function() {

        userInput.value = this.textContent.trim();

        sendMessage();
    });

});

// Focus input on page load
window.onload = () => {
    userInput.focus();
};

// Clear Chat Button
const clearChatBtn = document.getElementById("clearChatBtn");

clearChatBtn.addEventListener("click", () => {

    chatBox.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">
                <i class="bi bi-robot me-2"></i>
                Chat cleared successfully.
            </div>
        </div>
    `;

    userInput.value = "";
});