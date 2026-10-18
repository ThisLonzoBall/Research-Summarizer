# syntax=docker/dockerfile:1

# ---- Stage 1: build the React frontend ----
FROM node:20-slim AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- Stage 2: Python API serving the model and the built frontend ----
FROM python:3.11-slim

# Poppler + Tesseract enable OCR for scanned PDFs.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces runs containers as uid 1000.
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    HF_HOME=/home/user/.cache/huggingface \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /home/user/app

# CPU-only torch keeps the image ~2GB smaller than the default CUDA build.
RUN pip install --user torch --index-url https://download.pytorch.org/whl/cpu

COPY --chown=user requirements.txt pyproject.toml README.md LICENSE ./
COPY --chown=user src ./src
RUN pip install --user -r requirements.txt

COPY --chown=user app.py ./
COPY --chown=user --from=frontend /frontend/dist ./frontend/dist

# Override MODEL_ID with the fine-tuned Hub repo (Space settings → Variables).
ENV MODEL_ID=google/pegasus-cnn_dailymail \
    PORT=7860
EXPOSE 7860

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
