
// ========================================
// RAGdocAI - FRONTEND JAVASCRIPT
// ========================================


// ========================================
// 1. GET HTML ELEMENTS
// ========================================

const pdfUpload = document.getElementById("pdf-upload");
const questionInput = document.getElementById("question-input");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");
const themeToggle = document.getElementById("theme-toggle");


// Store uploaded document names
let uploadedFiles = [];


// ========================================
// 2. CHAT MESSAGE FUNCTION
// ========================================

function addMessage(message, type) {

    const messageDiv = document.createElement("div");

    messageDiv.className = `chat-message ${type}`;

    messageDiv.textContent = message;

    chatBox.appendChild(messageDiv);

    requestAnimationFrame(() => {
    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });
});

    return messageDiv;
}


// ========================================
// 3. PDF UPLOAD
// ========================================

pdfUpload.addEventListener("change", async function () {

    const files = Array.from(pdfUpload.files);

    if (files.length === 0) {
        return;
    }

    pdfUpload.disabled = true;

    let successfulUploads = [];

    for (const file of files) {

        if (!file.name.toLowerCase().endsWith(".pdf")) {

            addMessage(
                `${file.name}: Only PDF files are allowed.`,
                "system-message"
            );

            continue;
        }

        addMessage(
            `Uploading: ${file.name}`,
            "system-message"
        );

        const formData = new FormData();

        formData.append("file", file);

        try {

            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || "Upload failed.");
            }

            successfulUploads.push(result.filename);

            uploadedFiles.push(result.filename);

            addMessage(
                `Successfully processed: ${result.filename}\nChunks stored: ${result.total_chunks}`,
                "system-message"
            );

        } catch (error) {

            addMessage(
                `Failed to upload ${file.name}: ${error.message}`,
                "system-message"
            );

        }
    }

    if (successfulUploads.length > 0) {

        const filenames = successfulUploads.join(", ");

        addMessage(
            `Your documents are ready!\n\nYou can now ask questions about: ${filenames}`,
            "system-message"
        );

    }

    pdfUpload.value = "";

    pdfUpload.disabled = false;

});


// ========================================
// 4. ASK AI QUESTION
// ========================================

async function askQuestion() {

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage(question, "user-message");

    questionInput.value = "";

    sendBtn.disabled = true;

    const loadingMessage = addMessage(
        "Thinking... Please wait.",
        "system-message"
    );

    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Question processing failed.");
        }

        loadingMessage.remove();

        const answerParts = result.answer.split("\n\nSources:\n");

        const answerDiv = document.createElement("div");

        answerDiv.className = "chat-message ai-message";

        const answerText = document.createElement("p");

        answerText.textContent = answerParts[0];

        answerDiv.appendChild(answerText);

        // Display document sources
        if (answerParts.length > 1) {

            const sourceDiv = document.createElement("div");

            sourceDiv.className = "source-list";

            const sourceHeading = document.createElement("strong");

            sourceHeading.textContent = "Sources";

            sourceDiv.appendChild(sourceHeading);

            const sourceText = document.createElement("p");

            sourceText.textContent = answerParts.slice(1).join("\n\nSources:\n");

            sourceDiv.appendChild(sourceText);

            answerDiv.appendChild(sourceDiv);

        }

        chatBox.appendChild(answerDiv);

        requestAnimationFrame(() => {
            chatBox.scrollTo({
                top: chatBox.scrollHeight,
                behavior: "smooth"
            });
        });

    } catch (error) {

        loadingMessage.textContent =
            `Error: ${error.message}`;

    }

    sendBtn.disabled = false;

    questionInput.focus();

}


// ========================================
// 5. SEND BUTTON
// ========================================

sendBtn.addEventListener("click", askQuestion);


// ========================================
// 6. ENTER KEY TO SEND QUESTION
// ========================================

questionInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        askQuestion();
    }

});


// ========================================
// 7. CLICKABLE SUGGESTIONS
// ========================================

document.querySelectorAll(".suggestion").forEach(function (suggestion) {

    suggestion.addEventListener("click", function () {

        questionInput.value = suggestion.dataset.question;

        questionInput.focus();

    });

});


// ========================================
// 8. LIGHT / DARK THEME
// ========================================

const savedTheme = localStorage.getItem("ragdocai-theme");

if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
}


function updateThemeIcon() {

    if (document.body.classList.contains("dark-mode")) {

        themeToggle.textContent = "☀";

        themeToggle.title = "Switch to light mode";

    } else {

        themeToggle.textContent = "☾";

        themeToggle.title = "Switch to dark mode";

    }

}


themeToggle.addEventListener("click", function () {

    document.body.classList.toggle("dark-mode");

    const currentTheme =
        document.body.classList.contains("dark-mode")
            ? "dark"
            : "light";

    localStorage.setItem("ragdocai-theme", currentTheme);

    updateThemeIcon();

});


updateThemeIcon();


// Automatically focus question input when page loads
window.addEventListener("load", function () {
    questionInput.focus();
});