FROM python:3.12-alpine

COPY requirements.txt .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk update --no-cache && \
    apk upgrade --no-cache && \
#    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev linux-headers && \
    pip install --no-cache --index-url https://mirror-pypi.runflare.com/simple/ --upgrade pip && \
    pip install --no-cache-dir --index-url https://mirror-pypi.runflare.com/simple/ -r requirements.txt
#    apk del .build-deps
