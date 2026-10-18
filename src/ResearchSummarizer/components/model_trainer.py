import torch
from datasets import load_from_disk
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)

from ResearchSummarizer.entity import ModelTrainerConfig
from ResearchSummarizer.logging import logger


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    @staticmethod
    def _precision_args() -> dict:
        # Pegasus overflows in fp16, so only use mixed precision when bf16 is available.
        use_bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()
        return {"bf16": use_bf16, "fp16": False}

    def train(self) -> None:
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt)
        data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
        dataset = load_from_disk(self.config.data_path)

        training_args = Seq2SeqTrainingArguments(
            output_dir=str(self.config.root_dir / "checkpoints"),
            **self._precision_args(),
            **self.config.training_args,
        )
        logger.info(f"Training on {len(dataset['train'])} examples, device: {training_args.device}")

        trainer = Seq2SeqTrainer(
            model=model,
            args=training_args,
            train_dataset=dataset["train"],
            eval_dataset=dataset["validation"],
            data_collator=data_collator,
            processing_class=tokenizer,
        )
        trainer.train()

        trainer.save_model(str(self.config.model_dir))
        tokenizer.save_pretrained(str(self.config.model_dir))
        logger.info(f"Saved fine-tuned model to {self.config.model_dir}")
