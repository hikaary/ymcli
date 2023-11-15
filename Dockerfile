FROM python:3.11-slim as base

ARG app

RUN apt-get update && apt-get install -y x11-apps

# Устанавливаем зависимости
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential && \
  pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false
WORKDIR /app

COPY ./ ./
RUN poetry install
# Настройка переменной DISPLAY


CMD ["sh", "-c", "sleep infinity"]