from src.ResearchSummarizer.constants import *
from src.ResearchSummarizer.utils.common import read_yaml, create_directories

from src.ResearchSummarizer.entity import DataIngestionConfig, DataTransformationsConfig

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
