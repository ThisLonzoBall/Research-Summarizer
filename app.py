from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from src.ResearchSummarizer.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI(title="Research Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")



@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful !!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Occurred! {e}")



class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
async def predict_route(body: PredictRequest):
    try:
        obj = PredictionPipeline()
        summary = obj.predict(body.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)