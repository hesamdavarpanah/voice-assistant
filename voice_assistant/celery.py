from os import environ, getenv
from celery import Celery

environ.setdefault('DJANGO_SETTINGS_MODULE', f'{getenv("PROJECT_NAME")}.settings')
app = Celery(f'{getenv("PROJECT_NAME")}')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
