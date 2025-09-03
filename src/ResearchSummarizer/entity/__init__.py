from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: Path
    local_data_file: Path
    unzip_dir : Path

@dataclass
class DataTransformationsConfig:
    root_dir: Path
    data_path : Path
    tokenizer_name: Path
    
@dataclass
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    model_ckpt: Path
    num_train_epochs: int
    per_device_train_batch_size: int
    per_device_eval_batch_size: int
    evaluation_strategy: str
    eval_steps: int
    save_strategy: str
    save_steps: int
    learning_rate: float
    warmup_steps: int
    weight_decay: float
    logging_steps: int
    fp16: bool
    gradient_accumulation_steps: int
    predict_with_generate: bool
    load_best_model_at_end: bool
    metric_for_best_model: str
    report_to: str