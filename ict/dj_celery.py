from celery import Celery
import os
from ict.settings import DEBUG

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    "ict.envs.development" if DEBUG else "ict.envs.production"
)

app = Celery()
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
