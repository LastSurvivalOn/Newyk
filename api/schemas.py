from pydantic import BaseModel

class NewykTodayNewsRequest(BaseModel):
    url: str

class NewykTodayNewsResponse(BaseModel):
    news: list[dict[str, str|list[tuple[str, str]]]]|dict[str, str]
    
class NewykSummarizerRequest(BaseModel):
    text: str

class NewykSummarizerResponse(BaseModel):
    summary: str|dict[str, str]