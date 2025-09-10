from src.ResearchSummarizer.config.configuration import ConfigurationManager
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch

class PredictionPipeline:
    def __init__(self, num_beams=4, max_new_tokens=128, length_penalty=0.8):
        self.config = ConfigurationManager().get_model_evaluation_config()
        device = 0 if torch.cuda.is_available() else -1
        torch_dtype = torch.float16 if torch.cuda.is_available() else None
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.config.model_path,
            torch_dtype=torch_dtype
        )
        self.pipe = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,
            device=device
        )
        self.gen_kwargs = {
            "num_beams": num_beams,
            "max_new_tokens": max_new_tokens,
            "length_penalty": length_penalty,
            "early_stopping": True,
        }
        self.max_input_tokens = min(
            getattr(self.tokenizer, "model_max_length", 1024) or 1024,
            1024
        )
        self.chunk_overlap = 100

    def _token_len(self, text: str) -> int:
        return len(self.tokenizer(text, add_special_tokens=False)["input_ids"])

    def _chunk_text(self, text: str):
        ids = self.tokenizer(text, add_special_tokens=False)["input_ids"]
        stride = self.max_input_tokens - self.chunk_overlap
        chunks = []
        for start in range(0, len(ids), stride):
            end = start + self.max_input_tokens
            chunk_ids = ids[start:end]
            if not chunk_ids:
                break
            chunks.append(self.tokenizer.decode(chunk_ids, skip_special_tokens=True))
        return chunks

    def predict(self, text: str) -> str:
        if self._token_len(text) > self.max_input_tokens:
            chunks = self._chunk_text(text)
            partials = [
                self.pipe(c, **self.gen_kwargs)[0]["summary_text"].strip()
                for c in chunks
            ]
            joined = "\n".join(partials)
            return self.pipe(joined, **self.gen_kwargs)[0]["summary_text"].strip()
        return self.pipe(text, **self.gen_kwargs)[0]["summary_text"].strip()