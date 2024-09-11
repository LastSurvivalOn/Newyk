FROM python:3.11-slim

WORKDIR /NewykBot

RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && apt-get clean

COPY ./requirements/requirements.txt /NewykBot/requirements/requirements.txt

RUN apt update && \
  pip install --upgrade pip && \
  pip install --upgrade setuptools && \
  pip install --no-cache-dir --upgrade -r ./requirements/requirements.txt
    
COPY ./api /NewykBot/api
COPY ./sources /NewykBot/sources

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "9090"]