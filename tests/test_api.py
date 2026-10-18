import pytest
from fastapi.testclient import TestClient

import app as app_module

PAPER = "Transformers have become the dominant architecture for summarizing scientific articles. " * 3


class FakePipeline:
    model_id = "fake/model"

    def predict(self, text: str) -> str:
        return f"summary of {len(text.split())} words"


@pytest.fixture
def client():
    # TestClient without a context manager skips the lifespan, so no model is loaded.
    app_module.app.state.pipe = FakePipeline()
    yield TestClient(app_module.app)
    app_module.app.state.pipe = None


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok", "model": "fake/model"}


def test_summarize_text(client):
    resp = client.post("/api/summarize", json={"text": PAPER})
    assert resp.status_code == 200
    body = resp.json()
    assert body["summary"] == f"summary of {len(PAPER.split())} words"
    assert body["model"] == "fake/model"
    assert body["input_words"] == len(PAPER.split())


def test_summarize_text_rejects_short_input(client):
    assert client.post("/api/summarize", json={"text": "too short"}).status_code == 422


def test_pdf_rejects_non_pdf(client):
    resp = client.post("/api/summarize/pdf", files={"file": ("notes.pdf", b"hello", "application/pdf")})
    assert resp.status_code == 400


def test_pdf_rejects_oversized_upload(client, monkeypatch):
    monkeypatch.setattr(app_module, "MAX_UPLOAD_BYTES", 10)
    resp = client.post("/api/summarize/pdf", files={"file": ("big.pdf", b"%PDF-" + b"x" * 20, "application/pdf")})
    assert resp.status_code == 413


def test_pdf_without_text_returns_422(client, monkeypatch):
    monkeypatch.setattr(app_module, "load_pdf_as_block", lambda *a, **k: "   ")
    resp = client.post("/api/summarize/pdf", files={"file": ("scan.pdf", b"%PDF-1.4 ...", "application/pdf")})
    assert resp.status_code == 422


def test_pdf_happy_path(client, monkeypatch):
    monkeypatch.setattr(app_module, "load_pdf_as_block", lambda *a, **k: PAPER)
    resp = client.post("/api/summarize/pdf", files={"file": ("paper.pdf", b"%PDF-1.4 ...", "application/pdf")})
    assert resp.status_code == 200
    assert resp.json()["summary"].startswith("summary of")


def test_returns_503_while_model_loading(client):
    app_module.app.state.pipe = None
    assert client.post("/api/summarize", json={"text": PAPER}).status_code == 503
