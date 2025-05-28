FROM ict:1.0.0

WORKDIR /app

COPY . .

RUN adduser -D -H ict && \
    chown -R ict:ict /app

USER ict
