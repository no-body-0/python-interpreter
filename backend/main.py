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

@app.get("/")
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
@app.websocket("/ws/run")
async def run_terminal(ws: WebSocket):
    await ws.accept()
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("python", ["python"])
    try:
        while True:
            data = await ws.receive_text()
            if data == "__exit__":
                break
            os.write(fd, data.encode())
            await asyncio.sleep(0.01)
            try:
                output = os.read(fd, 1024).decode(errors="ignore")
                await ws.send_text(output)
            except OSError:
                break
    except:
        pass
