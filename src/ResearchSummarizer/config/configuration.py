from pathlib import Path

from ResearchSummarizer.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from ResearchSummarizer.entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    ModelEvaluationConfig,
    ModelTrainerConfig,
)
from ResearchSummarizer.utils.common import create_directories, read_yaml


class ConfigurationManager:
    def __init__(self, config_filepath: Path = CONFIG_FILE_PATH, params_filepath: Path = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        data = self.params.data
        create_directories([config.root_dir])
        return DataIngestionConfig(
            root_dir=Path(config.root_dir),
            dataset_name=config.dataset_name,
            dataset_config=config.dataset_config,
            save_dir=Path(config.save_dir),
            split_sizes={
                "train": data.train_samples,
                "validation": data.validation_samples,
                "test": data.test_samples,
            },
        )

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        data = self.params.data
        create_directories([config.root_dir])
        return DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            tokenizer_name=config.tokenizer_name,
            save_dir=Path(config.save_dir),
            max_input_length=data.max_input_length,
            max_target_length=data.max_target_length,
        )

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer
        create_directories([config.root_dir])
        return ModelTrainerConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            model_ckpt=config.model_ckpt,
            model_dir=Path(config.model_dir),
            training_args=self.params.TrainingArguments.to_dict(),
        )

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        create_directories([config.root_dir])
        return ModelEvaluationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            base_model=config.base_model,
            model_path=Path(config.model_path),
            metric_file_name=Path(config.metric_file_name),
            num_samples=self.params.evaluation.num_samples,
            batch_size=self.params.evaluation.batch_size,
            max_input_length=self.params.data.max_input_length,
            generation=self.params.generation.to_dict(),
        )
