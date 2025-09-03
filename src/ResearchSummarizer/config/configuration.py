from src.ResearchSummarizer.constants import *
from src.ResearchSummarizer.utils.common import read_yaml, create_directories

from src.ResearchSummarizer.entity import DataIngestionConfig, DataTransformationsConfig, ModelTrainerConfig

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        return DataIngestionConfig(
            root_dir=config.root_dir,
            source_url=config.source_url,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
    
    def get_data_transformations_config(self) -> DataTransformationsConfig:
        config= self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationsConfig(
            root_dir=config.root_dir,
            data_path= config.data_path,
            tokenizer_name= config.tokenizer_name
        )

        return data_transformation_config
    
    def get_model_trainer_config(self)  ->  ModelTrainerConfig:
        config=self.config.model_trainer
        params=self.params.TrainingArguments

        create_directories([config.root_dir])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_path=config.data_path,
            model_ckpt=config.model_ckpt,
            num_train_epochs= params.num_train_epochs,
            per_device_train_batch_size= params.per_device_train_batch_size,
            per_device_eval_batch_size= params.per_device_eval_batch_size,
            evaluation_strategy= params.evaluation_strategy,
            eval_steps= params.eval_steps,
            save_strategy= params.save_strategy,
            save_steps= params.save_steps,
            learning_rate= params.learning_rate,
            warmup_steps = params.warmup_steps,
            weight_decay = params.weight_decay,
            logging_steps = params.logging_steps,
            fp16 = params.fp16,
            gradient_accumulation_steps= params.gradient_accumulation_steps,
            predict_with_generate= params.predict_with_generate,
            load_best_model_at_end= params.load_best_model_at_end,
            metric_for_best_model= params.metric_for_best_model,
            report_to = params.report_to,

                
        )
        return model_trainer_config




