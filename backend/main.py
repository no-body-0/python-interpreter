import os
import uuid
import shutil
import asyncio
import pty
import subprocess
from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from github import Github
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return HTMLResponse("<h2>Python IDE Backend Running</h2>")
    
# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://no-body-0.github.io/python-interpreter/"],  # Or restrict to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# GitHub Gist token (set in Render Environment)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
g = Github(GITHUB_TOKEN)

# -------------------- Share endpoint --------------------
class Code(BaseModel):
    code: str

@app.post("/share")
def share_code(data: Code):
    gist = g.get_user().create_gist(
        public=True,
        files={f"code_{uuid.uuid4().hex}.py": {"content": data.code}},
        description="Shared Python code"
    )
    return {"url": gist.html_url, "raw": list(gist.files.values())[0].raw_url}

# -------------------- WebSocket live terminal --------------------
let ws;

function run() {
    const output = document.getElementById("output");
    output.textContent = "";

    // Open WebSocket
    ws = new WebSocket("wss://https://python-interpreter-t34q.onrender.com/ws/run");

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

