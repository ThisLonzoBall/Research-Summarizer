"""FastAPI service: summarize research papers from PDF uploads or pasted text."""

import asyncio
import os
import tempfile
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, File, HTTPException, Query, Request, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from ResearchSummarizer.utils.pdf_loader import load_pdf_as_block

MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_MB", "20")) * 1024 * 1024
MAX_TEXT_CHARS = 200_000
FRONTEND_DIST = Path(__file__).parent / "frontend" / "dist"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    from ResearchSummarizer.pipeline.prediction_pipeline import PredictionPipeline

    app.state.pipe = PredictionPipeline()
    yield


app = FastAPI(
    title="Research Summarizer",
    description="Abstractive summaries of research papers with a Pegasus model fine-tuned on arXiv.",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])

# The model is CPU/GPU bound and not safe to run concurrently; serialize requests.
inference_lock = asyncio.Lock()


class TextRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=MAX_TEXT_CHARS, description="Paper text to summarize")


class SummaryResponse(BaseModel):
    summary: str
    model: str
    input_words: int
    elapsed_seconds: float


class HealthResponse(BaseModel):
    status: Literal["ok", "loading"]
    model: str | None


async def _summarize(request: Request, text: str) -> SummaryResponse:
    pipe = getattr(request.app.state, "pipe", None)
    if pipe is None:
        raise HTTPException(status_code=503, detail="Model is still loading, try again shortly.")
    start = time.perf_counter()
    async with inference_lock:
        summary = await run_in_threadpool(pipe.predict, text)
    return SummaryResponse(
        summary=summary,
        model=pipe.model_id,
        input_words=len(text.split()),
        elapsed_seconds=round(time.perf_counter() - start, 2),
    )


@app.get("/api/health", response_model=HealthResponse)
async def health(request: Request):
    pipe = getattr(request.app.state, "pipe", None)
    return HealthResponse(status="ok" if pipe else "loading", model=getattr(pipe, "model_id", None))


@app.post("/api/summarize", response_model=SummaryResponse)
async def summarize_text(request: Request, body: TextRequest):
    return await _summarize(request, body.text)


@app.post("/api/summarize/pdf", response_model=SummaryResponse)
async def summarize_pdf(
    request: Request,
    file: UploadFile = File(..., description="Research paper as a PDF"),
    max_pages: int | None = Query(None, ge=1, le=200, description="Only read the first N pages"),
    ocr: Literal["auto", "never", "force"] = Query("auto", description="OCR pages without a text layer"),
):
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"PDF exceeds {MAX_UPLOAD_BYTES // (1024 * 1024)}MB limit.")
    if not content.startswith(b"%PDF"):
        raise HTTPException(status_code=400, detail="Please upload a valid PDF file.")

    with tempfile.TemporaryDirectory() as tmp_dir:
        pdf_path = Path(tmp_dir) / "upload.pdf"
        pdf_path.write_bytes(content)
        text = await run_in_threadpool(load_pdf_as_block, str(pdf_path), max_pages=max_pages, ocr_mode=ocr)

    if not text.strip():
        raise HTTPException(status_code=422, detail="No extractable text found in the PDF.")
    return await _summarize(request, text)


# Serve the built React app (single-container deploys); API routes above take precedence.
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
