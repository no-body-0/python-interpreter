function run() {
    fetch("https://python-interpreter-t34q.onrender.com/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: document.getElementById("code").value,
            stdin: document.getElementById("input").value
        })
    })
    .then(r => r.json())
    .then(d => {
        document.getElementById("output").textContent =
            (d.stdout || "") + (d.stderr || "");
    });
}
