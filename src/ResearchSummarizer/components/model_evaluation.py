import json

import evaluate
import pandas as pd
import torch
from datasets import load_from_disk
from tqdm import tqdm
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

from ResearchSummarizer.entity import ModelEvaluationConfig
from ResearchSummarizer.logging import logger

ROUGE_KEYS = ["rouge1", "rouge2", "rougeL", "rougeLsum"]


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    @staticmethod
    def _batches(items: list, batch_size: int):
        for i in range(0, len(items), batch_size):
            yield items[i : i + batch_size]

    def score_model(self, model_name_or_path: str, articles: list[str], references: list[str]) -> dict:
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path).to(self.device).eval()
        rouge = evaluate.load("rouge")

        batch_size = self.config.batch_size
        for article_batch, reference_batch in tqdm(
            zip(self._batches(articles, batch_size), self._batches(references, batch_size), strict=True),
            total=-(-len(articles) // batch_size),
            desc=str(model_name_or_path),
        ):
            inputs = tokenizer(
                article_batch,
                max_length=self.config.max_input_length,
                truncation=True,
                padding=True,
                return_tensors="pt",
            ).to(self.device)
            with torch.no_grad():
                outputs = model.generate(**inputs, **self.config.generation)
            predictions = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            predictions = [" ".join(p.split()) for p in predictions]
            rouge.add_batch(predictions=predictions, references=reference_batch)

        scores = rouge.compute(use_stemmer=True)
        return {k: round(float(scores[k]) * 100, 2) for k in ROUGE_KEYS}

    def evaluate(self) -> dict:
        test = load_from_disk(self.config.data_path)["test"]
        test = test.select(range(min(self.config.num_samples, len(test))))
        articles, references = test["article"], test["abstract"]

        results = {
            "base": self.score_model(self.config.base_model, articles, references),
            "fine-tuned": self.score_model(str(self.config.model_path), articles, references),
        }
        logger.info(f"ROUGE on {len(test)} test papers: {results}")

        with open(self.config.metric_file_name, "w", encoding="utf-8") as f:
            json.dump({"num_samples": len(test), "scores": results}, f, indent=2)
        pd.DataFrame(results).T.rename_axis("model").to_csv(self.config.metric_file_name.with_suffix(".csv"))
        return results
