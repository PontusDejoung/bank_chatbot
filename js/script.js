// script.js

// Selektorer för DOM-element
const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const startChatButton = document.querySelector("#start-chat-btn"); // Ny knapp för att starta konversation

let userText = null;

// Funktion för att initiera konversationen
const initializeConversation = () => {
    // Kontrollerar om det finns några sparade chattar
    if (!localStorage.getItem("all-chats")) {
        // Skapa ett initialt meddelande från chatbotten
        const welcomeMessage = "Hello! Welcome to our banking service. How can I assist you today?";
        const tempDiv = createChatElement(`<div class="chat-content">
                    <div class="chat-details">
                        <img src="images/chatbot.jpg" alt="chatbot-img">
                        <p>${sanitizeHTML(welcomeMessage)}</p>
                    </div>
                </div>`, "incoming");

        chatContainer.appendChild(tempDiv);
        localStorage.setItem("all-chats", chatContainer.innerHTML);
        chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scrolla till botten av chattbehållaren
    }
}

// Funktion för att ladda data från localStorage
const loadDataFromLocalstorage = () => {
    const themeColor = localStorage.getItem("themeColor");
    document.body.classList.toggle("light-mode", themeColor === "light_mode");
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";

    const defaultText = `<div class="default-text">
                            <h1>PontusGPT Using llama 3.1</h1>
                            <p>Start a conversation and explore the power of llama 3.1.<br> Your chat history will be displayed here.</p>
                        </div>`;

    chatContainer.innerHTML = localStorage.getItem("all-chats") || defaultText;
    chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scrollar till botten av chattbehållaren
    //initializeConversation();  // Startar en konversation om det inte finns någon historik
}

// Funktion för att skapa ett chatelement
const createChatElement = (content, className) => {
    // Skapa nytt div-element och applicera klassen
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv; // Returnera det skapade chatdiv-elementet
}

// Funktion för att hämta svar från backend
const getChatResponse = async (incomingChatDiv) => {
    const API_URL = "http://127.0.0.1:8000/get_response/";
    const pElement = document.createElement("p");

    // Hämta eller generera ett unikt användar-ID
    let userId = localStorage.getItem('userId');
    if (!userId) {
        userId = generateUserId();
        localStorage.setItem('userId', userId);
    }

    // Definiera egenskaperna och datan för API-förfrågan
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: userText,  // Antag att userText är definierad någon annanstans i din kod
            user_id: userId
        })
    };

    try {
        const response = await fetch(API_URL, requestOptions);
        if (!response.ok) {
            // Om statuskoden från svaret inte indikerar framgång, skapa ett fel
            throw new Error(`Server returned status ${response.status}`);
        }
        const responseData = await response.json();
        console.log("Response data:", responseData);
        
        // Hantera fel från servern om sådana finns
        if (responseData.error) {
            throw new Error(responseData.message);
        }

        // Hantera svaret baserat på typen av respons
        if (typeof responseData.response === 'string') {
            // Om svaret är en enkel sträng
            pElement.textContent = responseData.response;
        } else {
            // Om svaret är ett JSON-objekt, visa det snyggt
            pElement.textContent = JSON.stringify(responseData.response, null, 2);
        }

        // Uppdatera chatten
        incomingChatDiv.querySelector(".typing-animation").remove();
        incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
        localStorage.setItem("all-chats", chatContainer.innerHTML);
        chatContainer.scrollTo(0, chatContainer.scrollHeight);

    } catch (error) {
        console.error("Error fetching chat response:", error);
        pElement.classList.add("error");
        // Använd error.message för att visa mer specifik information om felet
        pElement.textContent = error.message || "An error occurred, please try again later.";
        incomingChatDiv.querySelector(".typing-animation").remove();
        incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    }
}

// Hjälpfunktion för att generera ett unikt användar-ID
function generateUserId() {
    return Math.random().toString(36).substring(2) + new Date().getTime().toString(36);
}

// Funktion för att kopiera svar till urklipp
const copyResponse = (copyBtn) => {
    // Kopiera textinnehållet i svaret till urklipp
    const responseTextElement = copyBtn.parentElement.querySelector("p");
    navigator.clipboard.writeText(responseTextElement.textContent);
    copyBtn.textContent = "done";
    setTimeout(() => copyBtn.textContent = "content_copy", 1000);
}

// Funktion för att visa skrivanimation
const showTypingAnimation = () => {
    // Visa skrivanimation och kalla på getChatResponse-funktionen
    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="images/chatbot.jpg" alt="chatbot-img">
                        <div class="typing-animation">
                            <div class="typing-dot" style="--delay: 0.2s"></div>
                            <div class="typing-dot" style="--delay: 0.3s"></div>
                            <div class="typing-dot" style="--delay: 0.4s"></div>
                        </div>
                    </div>
                    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
                </div>`;
    // Skapa ett inkommande chatdiv med skrivanimation och lägg till det i chattbehållaren
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    getChatResponse(incomingChatDiv);
}

// Funktion för att hantera utgående chattmeddelanden
const handleOutgoingChat = () => {
    userText = chatInput.value.trim(); // Hämta chatInput-värde och ta bort extra mellanslag
    if(!userText) return; // Om chatInput är tom, returnera härifrån

    // Rensa inmatningsfältet och återställ dess höjd
    chatInput.value = "";
    chatInput.style.height = `${initialInputHeight}px`;

    const html = `<div class="chat-content">
                    <div class="chat-details">
                        <img src="images/user.jpg" alt="user-img">
                        <p>${sanitizeHTML(userText)}</p>
                    </div>
                </div>`;

    // Skapa ett utgående chatdiv med användarens meddelande och lägg till det i chattbehållaren
    const outgoingChatDiv = createChatElement(html, "outgoing");
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    setTimeout(showTypingAnimation, 500);
}

// Eventlyssnare för radera-knappen
deleteButton.addEventListener("click", () => {
    // Bekräfta med användaren innan alla chattar raderas
    if(confirm("Är du säker på att du vill radera alla chattar?")) {
        localStorage.removeItem("all-chats");  // Ta bort alla chattar från localStorage
        const newUserId = generateUserId();  // Generera ett nytt användar-ID
        localStorage.setItem('userId', newUserId);  // Spara det nya användar-ID:t i localStorage
        loadDataFromLocalstorage();  // Ladda om standarddata för att återspegla förändringar
    }
});

// Eventlyssnare för temaknappen
themeButton.addEventListener("click", () => {
    // Växla kroppens klass för temaläge och spara den uppdaterade temat i localStorage
    document.body.classList.toggle("light-mode");
    const currentTheme = document.body.classList.contains("light-mode") ? "light_mode" : "dark_mode";
    localStorage.setItem("themeColor", currentTheme);
    themeButton.innerText = document.body.classList.contains("light-mode") ? "dark_mode" : "light_mode";
});

const initialInputHeight = chatInput.scrollHeight;

// Eventlyssnare för inmatningsfältets höjdjustering
chatInput.addEventListener("input", () => {   
    // Justera höjden på inmatningsfältet dynamiskt baserat på dess innehåll
    chatInput.style.height =  `${initialInputHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

// Eventlyssnare för tangentbordshändelser (Enter-tangenten)
chatInput.addEventListener("keydown", (e) => {
    // Om Enter-tangenten trycks utan Shift och fönsterbredden är större än 800 pixlar, hantera utgående chatt
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleOutgoingChat();
    }
});

// Initialisering av chattdata
loadDataFromLocalstorage();

// Eventlyssnare för skickaknappen
sendButton.addEventListener("click", handleOutgoingChat);

/**
 * Sanitize HTML to prevent XSS attacks
 * @param {string} str - The string to sanitize
 * @returns {string} - The sanitized string
 */
function sanitizeHTML(str) {
    const temp = document.createElement('div');
    temp.textContent = str;
    return temp.innerHTML;
}
