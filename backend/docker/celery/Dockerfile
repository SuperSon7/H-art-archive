FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements/development.txt .
RUN pip install --upgrade pip && pip install -r development.txt

COPY . .

# Celery 실행은 CMD에서 지정하지 않음