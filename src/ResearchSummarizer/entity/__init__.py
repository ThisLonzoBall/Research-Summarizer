from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    dataset_name: str
    dataset_config: str
    save_dir: Path
    split_sizes: dict[str, int]


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    tokenizer_name: str
    save_dir: Path
    max_input_length: int
    max_target_length: int


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_path: Path
    model_ckpt: str
    model_dir: Path
    training_args: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    data_path: Path
    base_model: str
    model_path: Path
    metric_file_name: Path
    num_samples: int
    batch_size: int
    max_input_length: int
    generation: dict = field(default_factory=dict)
