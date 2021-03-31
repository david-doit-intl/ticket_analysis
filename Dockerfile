FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN apt-get update && apt-get -yqq install gcc

WORKDIR /app

COPY pdm.lock pyproject.toml /app/

RUN pip -q install pdm

RUN pdm install

COPY generate.py .

CMD pdm run gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 generate:app
