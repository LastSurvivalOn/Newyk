from pydantic import BaseModel
from fastapi.responses import FileResponse

class NewykTodayNewsRequest(BaseModel):
    url: str

class NewykTodayNewsResponse(BaseModel):
    news: list[dict[str, str|list[tuple[str, str]]]]|dict[str, str]
    
class NewykSummarizerRequest(BaseModel):
    text: str

class NewykSummarizerResponse(BaseModel):
    summary: str|dict[str, str]
    
class NewykHTMLMakerResponse(BaseModel):
    html: dict[str, str]
    
class NewykSentimentAnalyzerRequest(BaseModel):
    text: str
    
class NewykSentimentAnalyzerResponse(BaseModel):
    sentiment: dict[str, float] | dict[str, str]