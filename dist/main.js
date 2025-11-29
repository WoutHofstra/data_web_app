"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
// Ensure this script runs after the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
    const sendBtn = document.getElementById("sendBtn");
    sendBtn?.addEventListener("click", handleSend);
});
function handleSend() {
    const input = document.getElementById("csvInput");
    const instructionsInput = document.getElementById("instructions");
    const output = document.getElementById("output");
    const aiImage = document.getElementById("aiImage"); // new img element
    if (!input.files || input.files.length === 0 || input.files[0] === undefined) {
        alert("Please select a CSV file!");
        return;
    }
    const csvFile = input.files[0];
    const instructions = instructionsInput.value.trim();
    if (!instructions) {
        alert("Please enter instructions!");
        return;
    }
    const formData = new FormData();
    formData.append("file", csvFile);
    formData.append("instructions", instructions);
    fetch("/analyze", {
        method: "POST",
        body: formData
    })
        .then(async (res) => {
        if (!res.ok) {
            throw new Error(`Server returned ${res.status}`);
        }
        let text = await res.text();
        // Remove surrounding quotes if present
        text = text.replace(/^"(.*)"$/, "$1");
        output.textContent = text;
        // If it looks like base64 PNG, display it
        if (text.startsWith("iVBOR")) { // typical PNG base64 prefix
            aiImage.src = "data:image/png;base64," + text;
            aiImage.style.display = "block";
        }
        else {
            aiImage.style.display = "none";
        }
    })
        .catch(err => {
        console.error("Error sending file:", err);
        output.textContent = "Error: " + err.message;
        aiImage.style.display = "none";
    });
}
//# sourceMappingURL=main.js.map