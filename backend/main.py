from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess, tempfile, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RunRequest(BaseModel):
    code: str
    stdin: str = ""

@app.get("/")
def root():
    return {"status": "Python IDE backend running"}

@app.post("/run")
def run_code(req: RunRequest):
    with tempfile.TemporaryDirectory() as tmp:
        file_path = os.path.join(tmp, "main.py")
        with open(file_path, "w") as f:
            f.write(req.code)

        try:
            result = subprocess.run(
                ["python", file_path],
                input=req.stdin,
                text=True,
                capture_output=True,
                timeout=5
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "Execution timed out"}
