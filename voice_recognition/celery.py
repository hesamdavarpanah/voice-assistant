from os import environ
from celery import Celery

environ.setdefault("DJANGO_SETTINGS_MODULES", "voice_recognition.settings")
app = Celery('voice_recognition')

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
