const editor = document.getElementById("editor");
const output = document.getElementById("output");
let ws;

function runCode() {
    output.textContent = "";
    ws = new WebSocket("wss://python-interpreter-t34q.onrender.com//ws/run");

    ws.onopen = () => {
        console.log("WebSocket connected!");
        const code = editor.value;
        code.split("\n").forEach(line => ws.send(line + "\n"));
        ws.send("__exit__\n");  // signal end
    };

    ws.onmessage = e => {
        output.textContent += e.data;
        output.scrollTop = output.scrollHeight;
    };

    ws.onerror = e => console.error("WS error", e);
    ws.onclose = () => console.log("WebSocket closed");
}

function shareCode() {
    fetch("https://python-interpreter-t34q.onrender.com//share", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({code: editor.value})
    })
    .then(res => res.json())
    .then(data => alert("Gist URL: " + data.url))
    .catch(err => console.error(err));
}
