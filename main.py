from src.ResearchSummarizer.logging import logger
from src.ResearchSummarizer.pipeline.state_1_data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.ResearchSummarizer.pipeline.stage_2_data_transformation_pipeline import DataTransformationTrainingPipeline
from src.ResearchSummarizer.pipeline.stage_3_model_trainer_pipeline import ModelTrainerTrainingPipeline
from src.ResearchSummarizer.pipeline.stage_4_model_evaluation_pipeline import ModelEvaluationTrainingPipeline

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

STAGE_NAME = "Model Trainer Stage"
try:
    logger.info(f"{STAGE_NAME} initiated.")
    model_trainer_pipeline = ModelTrainerTrainingPipeline()
    model_trainer_pipeline.initiate_model_trainer()
    logger.info(f"{STAGE_NAME} completed.")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Model Evaluation Stage"
try:
    logger.info(f"*****************")
    logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<<")
    model_evaluation = ModelEvaluationTrainingPipeline()
    model_evaluation.initiate_mode_evaluation()
    logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx=======x")
except Exception as e:
    logger.exception(e)
    raise e

