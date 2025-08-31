import os
from src.ResearchSummarizer.logging import logger
from transformers import AutoTokenizer
from datasets import load_from_disk

from src.ResearchSummarizer.entity import DataTransformationsConfig

class DataTransformation:
    def __init__(self, config:DataTransformationsConfig):
        self.config= config
        self.tokenizer= AutoTokenizer.from_pretrained(config.tokenizer_name)
    def tokenize(self, batch):
        inputs = ["summarize: " + doc for doc in batch["article"]]
        model_inputs = self.tokenizer(inputs, max_length=512, truncation=True, padding="max_length")
        labels = self.tokenizer(batch["abstract"], max_length=256, truncation=True, padding="max_length")
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    
    def convert(self):
        dataset= load_from_disk(self.config.data_path)
        dataset_pt = dataset.map(self.tokenize, batched= True)
        dataset_pt.save_to_disk(os.path.join(self.config.root_dir, "scientific_dataset"))
        