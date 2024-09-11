from pydantic import BaseModel

class NewykTodayNewsRequest(BaseModel):
    url: str

class NewykTodayNewsResponse(BaseModel):
    news: list[dict[str, str|list[tuple[str, str]]]]|dict[str, str]