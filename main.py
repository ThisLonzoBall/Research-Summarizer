from src.ResearchSummarizer.logging import logger
from src.ResearchSummarizer.pipeline.state_1_data_ingestion_pipeline import DataIngestionTrainingPipeline
STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f"{STAGE_NAME} initiated.")
    data_ingestion_pipeline = DataIngestionTrainingPipeline()
    data_ingestion_pipeline.initiate_data_ingestion()
    logger.info(f"{STAGE_NAME} completed.")
except Exception as e:
    logger.exception(e)
    raise e




