from datasets import load_from_disk
from transformers import AutoTokenizer

from ResearchSummarizer.entity import DataTransformationConfig
from ResearchSummarizer.logging import logger


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def tokenize(self, batch):
        # No padding here: DataCollatorForSeq2Seq pads each batch dynamically and
        # masks label padding with -100 so it is ignored by the loss.
        model_inputs = self.tokenizer(batch["article"], max_length=self.config.max_input_length, truncation=True)
        labels = self.tokenizer(
            text_target=batch["abstract"], max_length=self.config.max_target_length, truncation=True
        )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    def convert(self) -> None:
        dataset = load_from_disk(self.config.data_path)
        tokenized = dataset.map(
            self.tokenize,
            batched=True,
            remove_columns=dataset["train"].column_names,
        )
        tokenized.save_to_disk(self.config.save_dir)
        logger.info(f"Saved tokenized dataset to {self.config.save_dir}: {tokenized}")
