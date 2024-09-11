from fastapi import FastAPI, status
from api.parser import NewykParser as NewykParser
from api.schemas import NewykTodayNewsRequest as NewykTodayNewsRequest, NewykTodayNewsResponse as NewykTodayNewsResponse

app = FastAPI()
parser = NewykParser()

@app.get("/")
async def start():
    return "News Parser"

@app.get("/health/")
async def health():
    return status.HTTP_200_OK

@app.post("/get_news/")
async def get_news(request: NewykTodayNewsRequest) -> NewykTodayNewsResponse:
    response = parser(request.url)
    return NewykTodayNewsResponse(news=response)