from src.ResearchSummarizer.config.configuration import ConfigurationManager
from src.ResearchSummarizer.components.data_transformation import DataTransformation
from src.ResearchSummarizer.logging import logger

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        config=ConfigurationManager()
        data_transformation_config = config.get_data_transformations_config()
        data_transformation= DataTransformation(config=data_transformation_config)
        data_transformation.convert()
