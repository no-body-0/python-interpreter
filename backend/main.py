from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import asyncio, pty, os, uuid, subprocess, shutil
from github import Github
import os as sysos

# FastAPI app
app = FastAPI()

# CORS for frontend URL
FRONTEND_URL = "https://no-body-0.github.io/python-interpreter/"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Root route
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return HTMLResponse("<h2>Python IDE Backend Running</h2>")

# WebSocket for live code execution
@app.websocket("/ws/run")
async def run_terminal(ws: WebSocket):
    await ws.accept()
    pid, fd = pty.fork()
    if pid == 0:
        os.execvp("python", ["python"])
    try:
        while True:
            try:
                data = await ws.receive_text()
                if data.strip() == "__exit__":
                    break
                os.write(fd, data.encode())
                await asyncio.sleep(0.01)
                try:
                    output = os.read(fd, 1024).decode(errors="ignore")
                    await ws.send_text(output)
                except OSError:
                    break
            except Exception:
                break
    except:
        pass

# Share code via Gist
@app.post("/share")
async def share_code(code: str):
    token = sysos.environ.get("GITHUB_TOKEN")
    g = Github(token)
    gist = g.get_user().create_gist(
        public=True,
        files={"snippet.py": {"content": code}},
        description="Shared from Python IDE"
    )
    return {"url": gist.html_url}
