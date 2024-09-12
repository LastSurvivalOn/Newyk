from fastapi import FastAPI, status, BackgroundTasks
from api.parser import NewykParser as NewykParser
from api.html_maker import NewykHTMLMaker as NewykHTMLMaker
from api.schemas import NewykTodayNewsRequest as NewykTodayNewsRequest
from api.schemas import NewykTodayNewsResponse as NewykTodayNewsResponse
from api.schemas import NewykSummarizerRequest as NewykSummarizerRequest
from api.schemas import NewykSummarizerResponse as NewykSummarizerResponse
from api.summarizer import NewykSummarizer as NewykSummarizer
from api.schemas import NewykHTMLMakerResponse as NewykHTMLMakerResponse
from api.schemas import NewykSentimentAnalyzerRequest as NewykSentimentAnalyzerRequest
from api.schemas import NewykSentimentAnalyzerResponse as NewykSentimentAnalyzerResponse
from api.sentiment_analyzer import NewykSentimentAnalyzer as NewykSentimentAnalyzer
from fastapi.responses import FileResponse

app = FastAPI()
parser = NewykParser()
html_maker = NewykHTMLMaker()
summarizer = NewykSummarizer()
summarizer_response = summarizer.initialize()
sentiment_analyzer = NewykSentimentAnalyzer()
sentiment_analyzer_response = sentiment_analyzer.initialize()

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
async def get_news_html(request: NewykTodayNewsRequest, background_tasks: BackgroundTasks):
    response = parser(request.url)
    path_to_file_download = html_maker(response, save=True, temp=True)
    if type(path_to_file_download)==dict:
        return NewykHTMLMakerResponse(html=path_to_file_download)
    background_tasks.add_task(html_maker._remove_file_, path_to_file_download)
    return FileResponse(path=path_to_file_download, filename='Latest news.html', media_type='text/html')

@app.post("/summarize/")
async def summarize(request: NewykSummarizerRequest) -> NewykSummarizerResponse:
    if type(summarizer_response) == dict:
        return NewykSummarizerResponse(summary=summarizer_response)
    response = summarizer(request.text)
    return NewykSummarizerResponse(summary=response)

@app.post("/sentiment_analyze/")
async def sentiment_analyze(request: NewykSentimentAnalyzerRequest) -> NewykSentimentAnalyzerResponse:
    response = sentiment_analyzer(request.text)
    return NewykSentimentAnalyzerResponse(sentiment=response)

@app.post("/get_short_news/")
async def get_short_news(request: NewykTodayNewsRequest) -> NewykTodayNewsResponse:
    response = parser(request.url)
    if "Error" in response:
        return NewykTodayNewsResponse(news=response)
    
    for new in response:
        text = new["text"]
        summarized_text= summarizer(text)
        new["text"] = summarized_text
        sentiment = sentiment_analyzer(summarized_text)
        
        negative = sentiment["negative"]
        positive = sentiment["positive"]
        neutral = sentiment["neutral"]

        emoji = ""
        if negative > positive and negative > neutral:
            emoji = "😠" 
        elif positive > negative and positive > neutral:
            emoji = "😊" 
        else:
            emoji = "😐"
            
        new["sentiment"] = emoji
        
    return NewykTodayNewsResponse(news=response)