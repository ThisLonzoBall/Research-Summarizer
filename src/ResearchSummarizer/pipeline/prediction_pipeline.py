import os
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from ResearchSummarizer.logging import logger

LOCAL_MODEL_DIR = "artifacts/model_trainer/pegasus-arxiv"
BASE_MODEL_ID = "google/pegasus-cnn_dailymail"

MAX_INPUT_TOKENS = 1024
CHUNK_OVERLAP_TOKENS = 100
MAX_REDUCE_ROUNDS = 3


def resolve_model_id() -> str:
    """MODEL_ID env var (Hub repo or path) > local fine-tuned model > base checkpoint."""
    if model_id := os.getenv("MODEL_ID"):
        return model_id
    if Path(LOCAL_MODEL_DIR).exists():
        return LOCAL_MODEL_DIR
    logger.warning(f"No fine-tuned model found at {LOCAL_MODEL_DIR}; falling back to {BASE_MODEL_ID}")
    return BASE_MODEL_ID


class PredictionPipeline:
    """Summarizes arbitrarily long text with map-reduce over overlapping token windows."""

    def __init__(
        self, model_id: str | None = None, num_beams: int = 4, max_new_tokens: int = 256, length_penalty: float = 0.8
    ):
        self.model_id = model_id or resolve_model_id()
        use_cuda = torch.cuda.is_available()
        logger.info(f"Loading summarization model {self.model_id} on {'cuda' if use_cuda else 'cpu'}")

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.model_id)
        self.pipe = pipeline("summarization", model=model, tokenizer=self.tokenizer, device=0 if use_cuda else -1)
        self.gen_kwargs = {
            "num_beams": num_beams,
            "max_new_tokens": max_new_tokens,
            "length_penalty": length_penalty,
            "early_stopping": True,
            "truncation": True,
        }
        # Leave room for the EOS token the tokenizer appends.
        self.max_input_tokens = min(self.tokenizer.model_max_length or MAX_INPUT_TOKENS, MAX_INPUT_TOKENS) - 1

    def _token_ids(self, text: str) -> list[int]:
        return self.tokenizer(text, add_special_tokens=False)["input_ids"]

    def _chunk_text(self, text: str) -> list[str]:
        ids = self._token_ids(text)
        stride = self.max_input_tokens - CHUNK_OVERLAP_TOKENS
        return [
            self.tokenizer.decode(ids[start : start + self.max_input_tokens], skip_special_tokens=True)
            for start in range(0, max(len(ids) - CHUNK_OVERLAP_TOKENS, 1), stride)
        ]

    def _summarize(self, texts: list[str]) -> list[str]:
        outputs = self.pipe(texts, batch_size=4, **self.gen_kwargs)
        return [o["summary_text"].strip() for o in outputs]

    def predict(self, text: str) -> str:
        # Map: summarize each window. Reduce: summarize the joined partial summaries,
        # repeating while they still exceed the model's context window.
        for _ in range(MAX_REDUCE_ROUNDS):
            if len(self._token_ids(text)) <= self.max_input_tokens:
                break
            text = "\n".join(self._summarize(self._chunk_text(text)))
        return self._summarize([text])[0].replace("<n>", " ")
