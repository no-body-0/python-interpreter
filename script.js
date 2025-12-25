// CodeMirror editor
const editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    mode: "python",
    theme: "dracula",
    lineNumbers: true
});

// -------------------- WebSocket live run --------------------
let ws;

function run() {
    const output = document.getElementById("output");
    output.textContent = "";

    // Open WebSocket
    ws = new WebSocket("wss://YOUR_BACKEND_URL/ws/run");

    ws.onopen = () => {
        console.log("WebSocket connected!");

        // Send code line by line
        const code = editor.getValue();
        code.split("\n").forEach(line => {
            ws.send(line + "\n");
        });
    };

    ws.onmessage = (e) => {
        output.textContent += e.data;
        output.scrollTop = output.scrollHeight;
    };

    ws.onclose = () => console.log("WebSocket closed");
    ws.onerror = (err) => console.error("WebSocket error", err);
}

}

// -------------------- Share code --------------------
function share() {
    fetch("https://https://python-interpreter-t34q.onrender.com/share", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ code: editor.getValue() })
    })
    .then(res => res.json())
    .then(data => {
        navigator.clipboard.writeText(data.raw);
        alert("Link copied: " + data.raw);
    });
}
