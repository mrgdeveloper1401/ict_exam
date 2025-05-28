FROM ict:1.0.0

WORKDIR /app

COPY . .

RUN adduser -D -H ict && \
    chmod +x ./scripts/* && \
    chown -R ict:ict /app

USER ict
