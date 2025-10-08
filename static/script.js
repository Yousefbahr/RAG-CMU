const chatBox = document.getElementById("chat-box");
        const inputBox = document.getElementById("user-input");

        async function sendMessage() {
            const message = inputBox.value.trim();
            if (!message) return;

            appendMessage(message, 'user');

            inputBox.value = "";

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message })
                });

                const data = await response.json();
                appendMessage(data.response, 'bot');
            } catch (error) {
                appendMessage("Error: " + error.message, 'bot');
            }
        }

        function appendMessage(text, sender) {
            const msgDiv = document.createElement("div");
            msgDiv.classList.add("message");
            msgDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
            msgDiv.textContent = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        // Press Enter to send
        inputBox.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
            }
        });