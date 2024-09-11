from fastapi import FastAPI, status, BackgroundTasks
from api.parser import NewykParser as NewykParser
from api.html_maker import NewykHTMLMaker as NewykHTMLMaker
from api.schemas import NewykTodayNewsRequest as NewykTodayNewsRequest, NewykTodayNewsResponse as NewykTodayNewsResponse
from fastapi.responses import FileResponse

app = FastAPI()
parser = NewykParser()
html_maker = NewykHTMLMaker()

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

@app.post("/get_news_html/")
async def get_news_html(request: NewykTodayNewsRequest, background_tasks: BackgroundTasks) -> FileResponse:
    response = parser(request.url)
    path_to_file_download = html_maker(response, save=True, temp=True)
    background_tasks.add_task(html_maker._remove_file_, path_to_file_download)
    return FileResponse(path=path_to_file_download, filename='Latest news.html', media_type='text/html')