import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'New_HM.settings')

app = Celery('New_HM')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()