FROM python:3.10

WORKDIR /test_aiogram_bot

RUN apt update && \
    apt install libmaxminddb0 libmaxminddb-dev mmdb-bin curl redis-server -y && \
    pip install --upgrade pip && \
    pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false

COPY pyproject.toml /test_aiogram_bot
COPY poetry.lock /test_aiogram_bot

RUN poetry install

COPY . /test_aiogram_bot

CMD service redis-server start && python run.py
