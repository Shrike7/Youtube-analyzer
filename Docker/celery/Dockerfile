FROM python:3.11
LABEL authors="shrike"

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

COPY ./requirements.txt /app
RUN \
    set -eux \
    && apt-get update \
    && pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
COPY ../.. /app

ENTRYPOINT celery -A youtube_analyzer worker --concurrency=20 --loglevel=info