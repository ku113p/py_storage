import os
from pathlib import Path

import aiofiles
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

app = FastAPI()
ROOT = Path(os.getenv("STORAGE_DIR", "storage")).resolve()
ROOT.mkdir(parents=True, exist_ok=True)


def safe(path: str) -> Path:
    p = (ROOT / path).resolve()
    if not p.is_relative_to(ROOT):
        raise HTTPException(HTTP_400_BAD_REQUEST, "Invalid path")
    return p


def is_pdf(f: UploadFile) -> bool:
    return f.content_type == "application/pdf" and f.filename.lower().endswith(".pdf")


async def write_file(to: Path, f: UploadFile):
    async with aiofiles.open(to, "wb") as out:
        while chunk := await f.read(8192):
            await out.write(chunk)


def single_file(dir: Path) -> Path:
    files = [f for f in dir.iterdir() if f.is_file()]
    if len(files) == 1:
        return files[0]
    raise HTTPException(HTTP_404_NOT_FOUND, "Expected one file")


@app.get("/{path:path}/upload", response_class=HTMLResponse)
async def form(path: str):
    dir = safe(path)
    if dir.exists() and (not dir.is_dir() or any(dir.iterdir())):
        raise HTTPException(HTTP_409_CONFLICT, "Path in use")
    return HTMLResponse("""
        <html><body>
        <h2>Upload PDF</h2>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="application/pdf" required>
            <input type="submit" value="Upload">
        </form>
        </body></html>
    """)


@app.post("/{path:path}/upload")
async def upload(path: str, file: UploadFile):
    if not is_pdf(file):
        raise HTTPException(HTTP_400_BAD_REQUEST, "Only PDF allowed")

    dir = safe(path)
    if dir.exists() and (not dir.is_dir() or any(dir.iterdir())):
        raise HTTPException(HTTP_409_CONFLICT, "Path in use")

    dir.mkdir(parents=True, exist_ok=True)
    target = dir / Path(file.filename).name
    await write_file(target, file)
    return {"saved": str(target.relative_to(ROOT))}


@app.get("/{path:path}")
async def download(path: str):
    file = single_file(safe(path))
    return FileResponse(file, filename=file.name)
