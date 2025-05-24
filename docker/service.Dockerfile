FROM python:3.13-slim-alpine AS builder

WORKDIR /app

RUN apk add --no-cache \
    build-base \
    postgresql-dev

RUN pip install --upgrade poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi


FROM python:3.13-slim-alpine AS app

WORKDIR /app

RUN apk add --no-cache \
    libcairo2-dev

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /app /app
COPY --from=builder /usr/local/bin /usr/local/bin

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY . .
