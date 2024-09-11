from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from api.config import summarizer_model_path, summarizer_model_name

class NewykSummarizer:
    def __init__(self):
        self.model_directory = summarizer_model_path
    
    def initialize(self) -> dict[str, str] | None:
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_directory)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_directory)
        except Exception as e:
            return {"Error": f"Error with initializing summarizer: {str(e)}"}
        return None
    
    def save(self, save_directory: str = summarizer_model_path) -> dict[str, str] | None:
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(summarizer_model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(summarizer_model_name) 
        except Exception as e:
            return {"Error": f"Error with downloading summarizer: {str(e)}"}
        try:       
            self.tokenizer.save_pretrained(save_directory)
            self.model.save_pretrained(save_directory)
        except Exception as e:
            return {"Error": f"Error with saving summarizer: {str(e)}"}
        return None
    
    def __call__(self, text: str) -> str | dict[str, str]:
        try:
            text = text.replace("\"", "'")
            inputs = self.tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = self.model.generate(inputs["input_ids"], num_beams=4, max_length=142, early_stopping=True)
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary.strip()
        except Exception as e:
            return {"Error": f"Error with summarizing text: {str(e)}"}