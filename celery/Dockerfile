FROM celery_base:1.0.0

WORKDIR /home/celery

COPY . .

ENTRYPOINT ["celery", "-A", "/home/ict.dj_celery", "worker", "-l", "INFO"]