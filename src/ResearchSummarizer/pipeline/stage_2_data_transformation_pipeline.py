from ResearchSummarizer.components.data_transformation import DataTransformation
from ResearchSummarizer.config.configuration import ConfigurationManager


class DataTransformationTrainingPipeline:
    def run(self) -> None:
        config = ConfigurationManager().get_data_transformation_config()
        DataTransformation(config).convert()
