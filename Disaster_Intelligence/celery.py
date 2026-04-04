import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Disaster_Intelligence.settings')

app = Celery('Disaster_Intelligence')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()