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
    if (ws) ws.close();

    ws = new WebSocket("wss://YOUR_BACKEND_DOMAIN/ws/run");

    ws.onopen = () => {
        const code = editor.getValue();
        // Send code line by line
        code.split("\n").forEach(line => ws.send(line + "\n"));
    };

    ws.onmessage = (e) => {
        output.textContent += e.data;
        output.scrollTop = output.scrollHeight;
    };

    ws.onclose = () => console.log("Execution ended");
}

// -------------------- Share code --------------------
function share() {
    fetch("https://YOUR_BACKEND_DOMAIN/share", {
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
