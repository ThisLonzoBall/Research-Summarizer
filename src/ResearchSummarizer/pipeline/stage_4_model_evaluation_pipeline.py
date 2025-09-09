from src.ResearchSummarizer.config.configuration import ConfigurationManager
from src.ResearchSummarizer.components.model_evaluation import ModelEvaluation
from src.ResearchSummarizer.logging import logger

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass
    
    def initiate_mode_evaluation(self):
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()   
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate()