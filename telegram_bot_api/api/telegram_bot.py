import os
import telebot
from dotenv import load_dotenv
import requests
import json

load_dotenv("telegram_bot_api/.env")

BOT_TOKEN = os.environ.get('BOT_TOKEN')
NEWYK_API_URL = os.environ.get('NEWYK_API_URL')

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    
@bot.message_handler(func=lambda message: message.text.strip().lower() == "hello")
def reply_hello(message):
    bot.reply_to(message, "Hello! How can I help you?")
    
@bot.message_handler(commands=['summarize'])
def summarize_handler(message):
    text = "Please enter the text you want to summarize."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
    sent_msg, fetch_summarizing_text)
    
def fetch_summarizing_text(message):
    text = message.text
    summ_text = get_summarized_text(text)
    bot.send_message(message.chat.id, "Here's your summarised text!")
    bot.send_message(message.chat.id, summ_text, parse_mode="Markdown")
    
def get_summarized_text(text: str) -> dict:
    url = f"{NEWYK_API_URL}/summarize/"
    params = {"text": text}
    response = requests.post(url, json=params).json()
    response = response["summary"]
    return response

@bot.message_handler(commands=['get_news'])
def get_news_handler(message):
    url = f"{NEWYK_API_URL}/get_news_html/"
    params = {"url": "https://www.bbc.com/"}
    response = requests.post(url, json=params)
    bot.send_document(message.chat.id, response.content, visible_file_name="Last News.html")
    

@bot.message_handler(commands=['today_news'])
def today_news_handler(message):
    # url = f"{NEWYK_API_URL}/get_short_news/"
    # params = {"url": "https://www.bbc.com/"}
    # response = requests.post(url, json=params)
    with open("telegram_bot_api/news.json", "r", encoding="utf-8") as file:
        response = json.load(file)
    for new in response['news']:
        title = new["title"]
        text = new["text"]
        images = new["images"]
        url = new["url"]
        sentiment = new["sentiment"]
        if images:
            bot.send_photo(message.chat.id, photo=images[0][0], caption=f"{title}\n{text}\n{sentiment*3}\nRead more: {url}")
        else:
            bot.send_message(message.chat.id, f"{title}\n{text}\n{sentiment*3}\nRead more: {url}")


bot.infinity_polling()