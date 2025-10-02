document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("akasha-form");
    const input = document.getElementById("akasha-terminal-input-field");
    const chatWindow = document.getElementById("akasha-chat-window");

    form.addEventListener("submit", async function(event) {
        event.preventDefault();
        
        let userMessage = input.value.trim();
        if (!userMessage) return;

        // Show user message immediately
        chatWindow.innerHTML += `<div class="user-message">${userMessage}</div>`;

        // Clear input
        input.value = "";

        // Send to backend
        let response = await fetch("/ask-akasha", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                "akasha-terminal-input-field": userMessage
            })
        });

        let data = await response.json();

        // Show Akasha's reply
        if (data.akasha_response) {
            chatWindow.innerHTML += `<div class="akasha-message">${data.akasha_response}</div>`;
        }

        // Auto-scroll to bottom
        chatWindow.scrollTop = chatWindow.scrollHeight;

        console.log("Backend full response:", data);
        console.log("Akasha says:", data.akasha_response);
        console.log("TYPE:", typeof data.akasha_response);

    });
});