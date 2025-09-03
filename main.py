from src.ResearchSummarizer.logging import logger
from src.ResearchSummarizer.pipeline.state_1_data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.ResearchSummarizer.pipeline.stage_2_data_transformation_pipeline import DataTransformationTrainingPipeline
from src.ResearchSummarizer.pipeline.stage_3_model_trainer_pipeline import ModelTrainerTrainingPipeline

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f"{STAGE_NAME} initiated.")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(f"{STAGE_NAME} completed.")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Transformation Stage"
try:
    logger.info(f"{STAGE_NAME} initiated.")
    data_ingestion_pipeline = DataTransformationTrainingPipeline()
    data_ingestion_pipeline.initiate_data_transformation()
    logger.info(f"{STAGE_NAME} completed.")
except Exception as e:
    logger.exception(e)
    raise e

#STAGE_NAME = "Model Trainer Stage"
#try:
    #logger.info(f"{STAGE_NAME} initiated.")
    #model_trainer_pipeline = ModelTrainerTrainingPipeline()
    #model_trainer_pipeline.initiate_model_trainer()
    #logger.info(f"{STAGE_NAME} completed.")
#except Exception as e:
    #logger.exception(e)
    #raise e

