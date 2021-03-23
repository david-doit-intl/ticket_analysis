FROM python:3.8-slim-buster as builder

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip -q install poetry

RUN poetry export -f requirements.txt --without-hashes --output requirements.txt

FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN pip -q install -r requirements.txt

COPY generate.py .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 0 generate:app
