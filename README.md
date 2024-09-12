# Newyk Bot

Newyk Bot is a Telegram bot that parses news from BBC, provides summarized and analyzed news articles directly in chat, generates HTML reports, and performs text summarization and sentiment analysis.

## Features

- **News Parsing from BBC**: Fetches and parses the latest news articles from BBC.
- **Summarized News**: Summarizes long articles for a quick read.
- **HTML File Generation**: Generates an HTML file that contains formatted news data for easy sharing.
- **Sentiment Analysis**: Analyzes the tone of the news articles (Positive, Negative, Neutral).
- **News Delivery in Chat**: Delivers the latest news with headlines, images, summaries, and links to the full article directly in the chat.

## Getting Started

### Prerequisites

To run Newyk Bot, you need the following:
- Docker
- Make

If you don't have Docker installed, you can follow the [official Docker installation guide](https://docs.docker.com/get-docker/).

### Installation

#### 1. Clone this repository:

```bash
git clone https://github.com/LastSurvivalOn/Newyk.git
cd Newyk
```

#### 2. Build your Docker-container:
```bash
make build
```

#### 3. Up your Docker-container:
```bash
make up
```

#### 4. Enable logging:
```bash
make logs
```

#### 5. If you wanna to use tg-bot, yoy need to get token and put it in telegram_bot_api/.env and install all requirements from telegram_bot_api and run telegram_bot_api/api/telegram_bot.py

![Alt text](background.webp)


