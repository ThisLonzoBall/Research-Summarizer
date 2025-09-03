from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import DataCollatorForSeq2Seq
from nltk.tokenize import sent_tokenize
import torch
import numpy
from datasets import load_from_disk
import os
import evaluate
from src.ResearchSummarizer.entity import ModelTrainerConfig


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
    
    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu" 
        tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

        #loading the data
        dataset_scientific_pt = load_from_disk(self.config.data_path)

        
        training_args = Seq2SeqTrainingArguments(
            output_dir=self.config.root_dir,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            per_device_eval_batch_size=4,
            eval_strategy='epoch',  
            save_strategy='epoch',        
            learning_rate=5e-5,
            warmup_steps=50,
            weight_decay=0.01,
            logging_steps=20,
            fp16=True,
            gradient_accumulation_steps=2,
            predict_with_generate=True,
            load_best_model_at_end=True,
            metric_for_best_model='eval_loss',
            report_to="none"
        )

        rouge_metric = evaluate.load("rouge")

        def compute_metrics(eval_pred):
            predictions, labels = eval_pred
            decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
            labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
            decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
            decoded_preds = ["\n".join(sent_tokenize(pred.strip())) for pred in decoded_preds]
            decoded_labels = ["\n".join(sent_tokenize(label.strip())) for label in decoded_labels]
            result = rouge_metric.compute(
                predictions=decoded_preds,
                references=decoded_labels,
                use_stemmer=True
            )
            result = {key: value * 100 for key, value in result.items()}
            return {k: round(v, 4) for k, v in result.items()}

        trainer = Seq2SeqTrainer(
            model=model_pegasus,
            args=training_args,
            train_dataset=dataset_scientific_pt["train"],
            eval_dataset=dataset_scientific_pt["validation"],
            data_collator=seq2seq_data_collator,
            tokenizer=tokenizer,
            compute_metrics=compute_metrics
        )

        trainer.train()

        model_pegasus.save_trained(os.path.join(self.config.root_dir, "pegasus-scientific-model"))

        tokenizer.save_pretrained(os.path.join(self.config.root_dir, "tokenizer"))
