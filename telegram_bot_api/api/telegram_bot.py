import os
import telebot
from dotenv import load_dotenv
import requests

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

bot.infinity_polling()