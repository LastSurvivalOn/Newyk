from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from api.config import sentiment_analyzer_model_name, sentiment_analyzer_model_task, sentiment_analyzer_model_path
from pathlib import Path

class NewykSentimentAnalyzer:
    def __init__(self):
        self.model_directory = sentiment_analyzer_model_path
    
    def initialize(self) -> dict[str, str] | None:
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_directory)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_directory)
            self.classifier = pipeline(
                                task="zero-shot-classification",
                                model=self.model,
                                tokenizer=self.tokenizer
                                )
        except Exception as e:
            try:
                self.save()
            except Exception as e:
                return {"Error": f"Error with initializing semantic analyzer: {str(e)}"}
        return None
    
    def save(self, save_directory: str = sentiment_analyzer_model_path) -> dict[str, str] | None:
        try:
            self.classifier = pipeline(
                                task=sentiment_analyzer_model_task,
                                model=sentiment_analyzer_model_name
                                )
        except Exception as e:
            return {"Error": f"Error with downloading semantic analyzer: {str(e)}"}
        try:
            directory = Path(save_directory)
            directory.mkdir(parents=True, exist_ok=True)
            self.classifier.tokenizer.save_pretrained(save_directory)
            self.classifier.model.save_pretrained(save_directory)
        except Exception as e:
            return {"Error": f"Error with saving semantic analyzer: {str(e)}"}
        return None
    
    def __call__(self, text: str) -> dict[str, float] | dict[str, str]:
        try:
            text = text.replace("\"", "'")
            result = self.classifier(text, ["positive", "negative", "neutral"], multi_class=True)
            print(result['scores'], result['labels'])
            dict_of_results = dict(zip(result['labels'], result['scores']))
            return dict_of_results
        except Exception as e:
            return {"Error": f"Error with analyzing text: {str(e)}"}
