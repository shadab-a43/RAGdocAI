
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

const documentCount = document.getElementById("document-count");
const documentsList = document.getElementById("uploaded-documents-list");


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
// 3. DOCUMENT MANAGER
// ========================================

// Fetch and display uploaded PDFs

async function fetchDocuments() {

    try {

        const response = await fetch("/documents");

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Unable to load documents."
            );
        }

        renderDocuments(result.documents);

        documentCount.textContent = result.total_documents;

    } catch (error) {

        documentsList.textContent = "Unable to load documents.";

        documentCount.textContent = "0";

        addMessage(
            `Document list error: ${error.message}`,
            "system-message"
        );

    }

}


// Display document cards

function renderDocuments(documents) {

    documentsList.innerHTML = "";

    if (!documents || documents.length === 0) {

        const emptyMessage = document.createElement("div");

        emptyMessage.className = "documents-empty";

        emptyMessage.textContent = "No documents uploaded yet.";

        documentsList.appendChild(emptyMessage);

        return;
    }

    documents.forEach(function (doc) {

        const card = document.createElement("div");

        card.className = "document-card";

        // PDF icon

        const icon = document.createElement("div");

        icon.className = "document-icon";

        icon.textContent = "📄";

        // Document information

        const info = document.createElement("div");

        info.className = "document-info";

        const name = document.createElement("span");

        name.className = "document-name";

        name.textContent = doc.filename;

        const chunks = document.createElement("span");

        chunks.className = "document-chunks";

        chunks.textContent = `${doc.total_chunks} chunks`;

        info.appendChild(name);

        info.appendChild(chunks);

        // Delete button

        const deleteButton = document.createElement("button");

        deleteButton.className = "delete-document-btn";

        deleteButton.textContent = "🗑";

        deleteButton.title = "Delete this PDF";

        deleteButton.setAttribute(
            "aria-label",
            `Delete ${doc.filename}`
        );

        deleteButton.addEventListener("click", function () {

            deleteDocument(doc, deleteButton);

        });

        card.appendChild(icon);

        card.appendChild(info);

        card.appendChild(deleteButton);

        documentsList.appendChild(card);

    });

}


// ========================================
// 4. DELETE SELECTED DOCUMENT
// ========================================

async function deleteDocument(doc, deleteButton) {

    const confirmed = window.confirm(
        `Are you sure you want to permanently delete "${doc.filename}"?\n\nThis will remove the PDF and all its stored chunks.`
    );

    if (!confirmed) {
        return;
    }

    deleteButton.disabled = true;

    try {

        const response = await fetch(
            `/documents/${encodeURIComponent(doc.document_id)}`,
            {
                method: "DELETE"
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "Document deletion failed."
            );
        }

        addMessage(
            `Deleted: ${result.filename}\nChunks removed: ${result.deleted_chunks}`,
            "system-message"
        );

        // Refresh document list and count

        await fetchDocuments();

    } catch (error) {

        addMessage(
            `Delete failed: ${error.message}`,
            "system-message"
        );

        deleteButton.disabled = false;

    }

}


// ========================================
// 5. PDF UPLOAD
// ========================================

pdfUpload.addEventListener("change", async function () {

    const files = Array.from(pdfUpload.files);

    if (files.length === 0) {
        return;
    }

    pdfUpload.disabled = true;

    // Store successfully uploaded or already available documents

    const readyDocuments = [];

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
                throw new Error(
                    result.detail || "Upload failed."
                );
            }

            // Handle duplicate PDF

            if (result.duplicate) {

                addMessage(
                    `Duplicate detected! Already uploaded as: ${result.filename}\n${result.message}`,
                    "system-message"
                );

                readyDocuments.push(result.filename);

                continue;
            }

            // Store successful upload filename

            readyDocuments.push(result.filename);

        } catch (error) {

            addMessage(
                `Failed to upload ${file.name}: ${error.message}`,
                "system-message"
            );

        }

    }

    // Show one final confirmation after all uploads

    if (readyDocuments.length > 0) {

        addMessage(
            `Your documents are ready!\n\nYou can now ask questions about: ${readyDocuments.join(", ")}`,
            "system-message"
        );

        // Refresh document manager only once

        await fetchDocuments();

    }

    pdfUpload.value = "";

    pdfUpload.disabled = false;

});


// ========================================
// 6. ASK AI QUESTION
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
            throw new Error(
                result.detail || "Question processing failed."
            );
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
// 7. SEND BUTTON
// ========================================

sendBtn.addEventListener("click", askQuestion);


// ========================================
// 8. ENTER KEY TO SEND QUESTION
// ========================================

questionInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        askQuestion();
    }

});


// ========================================
// 9. CLICKABLE SUGGESTIONS
// ========================================

document.querySelectorAll(".suggestion").forEach(function (suggestion) {

    suggestion.addEventListener("click", function () {

        questionInput.value = suggestion.dataset.question;

        questionInput.focus();

    });

});


// ========================================
// 10. LIGHT / DARK THEME
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


// ========================================
// 11. INITIALIZE APPLICATION
// ========================================

window.addEventListener("load", function () {

    // Load uploaded PDFs

    fetchDocuments();

    // Focus question input

    questionInput.focus();

});
