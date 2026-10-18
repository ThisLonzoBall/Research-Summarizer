from ResearchSummarizer.components.model_evaluation import ModelEvaluation
from ResearchSummarizer.config.configuration import ConfigurationManager


class ModelEvaluationTrainingPipeline:
    def run(self) -> None:
        config = ConfigurationManager().get_model_evaluation_config()
        ModelEvaluation(config).evaluate()
