FROM ict:1.0.0

WORKDIR /app

COPY . .

RUN adduser -D -H ict && \
    chmod +x ./scripts/* && \
    chown -R ict:ict /app && \
    pip install --no-cache --index-url https://mirror-pypi.runflare.com/simple/ django-axes

USER ict
