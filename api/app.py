from fastapi import FastAPI, status, BackgroundTasks
from api.parser import NewykParser as NewykParser
from api.html_maker import NewykHTMLMaker as NewykHTMLMaker
from api.schemas import NewykTodayNewsRequest as NewykTodayNewsRequest
from api.schemas import NewykTodayNewsResponse as NewykTodayNewsResponse
from api.schemas import NewykSummarizerRequest as NewykSummarizerRequest
from api.schemas import NewykSummarizerResponse as NewykSummarizerResponse
from api.summarizer import NewykSummarizer as NewykSummarizer
from fastapi.responses import FileResponse

app = FastAPI()
parser = NewykParser()
html_maker = NewykHTMLMaker()
summarizer = NewykSummarizer()
summarizer_response = summarizer.initialize()

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

@app.post("/summarize/")
async def summarize(request: NewykSummarizerRequest) -> NewykSummarizerResponse:
    if type(summarizer_response) == dict:
        return NewykSummarizerResponse(summary=summarizer_response)
    response = summarizer(request.text)
    return NewykSummarizerResponse(summary=response)