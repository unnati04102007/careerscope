document.addEventListener('DOMContentLoaded', () => {
    // Inject HTML Logic for Chatbot
    const chatbotContainer = document.getElementById('chatbot-container');
    chatbotContainer.innerHTML = `
        <button class="chatbot-toggler">
            <span class="material-symbols-rounded"><i class="fas fa-comment"></i></span>
            <span class="material-symbols-outlined"><i class="fas fa-times"></i></span>
        </button>
        <div class="chatbot">
            <header>
                <h2>Chat AI</h2>
                <span class="close-btn material-symbols-outlined"><i class="fas fa-times"></i></span>
            </header>
            <ul class="chatbox">
                <li class="chat incoming">
                    <span class="material-symbols-outlined"><i class="fas fa-robot"></i></span>
                    <p>Hi there 👋<br>How can I help you today?</p>
                </li>
            </ul>
            <div class="chat-input">
                <textarea placeholder="Enter a message..." spellcheck="false" required></textarea>
                <span id="send-btn" class="material-symbols-rounded"><i class="fas fa-paper-plane"></i></span>
            </div>
        </div>
    `;

    const chatbotToggler = document.querySelector(".chatbot-toggler");
    const closeBtn = document.querySelector(".close-btn");
    const chatbox = document.querySelector(".chatbox");
    const chatInput = document.querySelector(".chat-input textarea");
    const sendChatBtn = document.querySelector(".chat-input span");

    let userMessage = null; // Variable to store user's message

    const createChatLi = (message, className) => {
        // Create a chat <li> element with passed message and className
        const chatLi = document.createElement("li");
        chatLi.classList.add("chat", `${className}`);
        let chatContent = className === "outgoing"
            ? `<p></p>`
            : `<span class="material-symbols-outlined"><i class="fas fa-robot"></i></span><p></p>`;
        chatLi.innerHTML = chatContent;
        chatLi.querySelector("p").textContent = message;
        // Allow HTML for incoming messages to support formatting
        if (className === "incoming") {
            chatLi.querySelector("p").innerHTML = message.replace(/\n/g, '<br>');
        }
        return chatLi;
    }

    const generateResponse = (chatElement) => {
        const API_URL = "/api/chat";
        const messageElement = chatElement.querySelector("p");

        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: userMessage
            })
        }

        // Send POST request to API, get response and set response as paragraph text
        fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
            // Apply simple markdown formatting (Bold **text**)
            let formattedReply = data.reply.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
            // List formatting
            formattedReply = formattedReply.replace(/\n-/g, '<br>•');

            messageElement.innerHTML = formattedReply;
        }).catch(() => {
            messageElement.classList.add("error");
            messageElement.textContent = "Oops! Something went wrong. Please try again.";
        }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
    }

    const handleChat = () => {
        userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
        if (!userMessage) return;

        // Clear the input textarea and set its height to default
        chatInput.value = "";
        chatInput.style.height = "auto";

        // Append the user's message to the chatbox
        chatbox.appendChild(createChatLi(userMessage, "outgoing"));
        chatbox.scrollTo(0, chatbox.scrollHeight);

        setTimeout(() => {
            // Display "Thinking..." message while waiting for the response
            const incomingChatLi = createChatLi("Thinking...", "incoming");
            chatbox.appendChild(incomingChatLi);
            chatbox.scrollTo(0, chatbox.scrollHeight);
            generateResponse(incomingChatLi);
        }, 600);
    }

    chatInput.addEventListener("input", () => {
        // Adjust the height of the input textarea based on its content
        chatInput.style.height = `${chatInput.scrollHeight}px`;
    });

    chatInput.addEventListener("keydown", (e) => {
        // If Enter key is pressed without Shift key and the window 
        // width is greater than 800px, handle the chat
        if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
            e.preventDefault();
            handleChat();
        }
    });

    sendChatBtn.addEventListener("click", handleChat);
    closeBtn.addEventListener("click", () => document.body.classList.remove("show-chatbot"));
    chatbotToggler.addEventListener("click", () => document.body.classList.toggle("show-chatbot"));
});
