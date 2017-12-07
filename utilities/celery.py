import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'user_accounts.settings')

app = Celery()
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()

