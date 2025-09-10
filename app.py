from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, tempfile

from src.ResearchSummarizer.pipeline.prediction_pipeline import PredictionPipeline
from src.ResearchSummarizer.utils.pdf_loader import load_pdf_as_block


app = FastAPI(title="Research Summarizer")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

pipe: PredictionPipeline | None = None

@app.on_event("startup")
def _load_model_once():
    global pipe
    pipe = PredictionPipeline()

@app.get("/")
async def index():
    return RedirectResponse(url="/docs")

@app.post("/pdf/summary")
async def summarize_pdf(
    file: UploadFile = File(...),
    max_pages: int | None = Query(None, ge=1, description="Cap pages for speed"),
    ocr: str = Query("auto", pattern="^(auto|never|force)$"),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a .pdf file.")
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        text = load_pdf_as_block(tmp_path, max_pages=max_pages, ocr_mode=ocr)
        if not text.strip():
            raise HTTPException(status_code=422, detail="No extractable text found.")
        summary = pipe.predict(text)
        return {"summary": summary}
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)