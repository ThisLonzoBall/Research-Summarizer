from ResearchSummarizer.components.model_trainer import ModelTrainer
from ResearchSummarizer.config.configuration import ConfigurationManager


class ModelTrainerTrainingPipeline:
    def run(self) -> None:
        config = ConfigurationManager().get_model_trainer_config()
        ModelTrainer(config).train()
