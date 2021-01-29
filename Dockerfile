FROM python:3.8-slim-buster as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY generate.py .

ENTRYPOINT ["python", "/app/generate.py"]
