from ResearchSummarizer.components.data_ingestion import DataIngestion
from ResearchSummarizer.config.configuration import ConfigurationManager


class DataIngestionTrainingPipeline:
    def run(self) -> None:
        config = ConfigurationManager().get_data_ingestion_config()
        DataIngestion(config).download_dataset()
