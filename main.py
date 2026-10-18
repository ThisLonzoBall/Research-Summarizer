"""Run the training pipeline: ingestion -> transformation -> training -> evaluation.

Usage:
    python main.py                      # all stages
    python main.py --stage train eval   # selected stages
"""

import argparse

from ResearchSummarizer.logging import logger
from ResearchSummarizer.pipeline.stage_1_data_ingestion_pipeline import DataIngestionTrainingPipeline
from ResearchSummarizer.pipeline.stage_2_data_transformation_pipeline import DataTransformationTrainingPipeline
from ResearchSummarizer.pipeline.stage_3_model_trainer_pipeline import ModelTrainerTrainingPipeline
from ResearchSummarizer.pipeline.stage_4_model_evaluation_pipeline import ModelEvaluationTrainingPipeline

STAGES = {
    "ingest": ("Data Ingestion", DataIngestionTrainingPipeline),
    "transform": ("Data Transformation", DataTransformationTrainingPipeline),
    "train": ("Model Training", ModelTrainerTrainingPipeline),
    "eval": ("Model Evaluation", ModelEvaluationTrainingPipeline),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stage", nargs="+", choices=STAGES, default=list(STAGES), help="stages to run, in order")
    args = parser.parse_args()

    for key in args.stage:
        name, pipeline_cls = STAGES[key]
        logger.info(f">>>>> {name} stage started <<<<<")
        try:
            pipeline_cls().run()
        except Exception:
            logger.exception(f"{name} stage failed")
            raise
        logger.info(f">>>>> {name} stage completed <<<<<")


if __name__ == "__main__":
    main()
