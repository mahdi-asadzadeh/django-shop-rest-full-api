from django.conf import settings
import os
from datetime import timedelta
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.autodiscover_tasks()

if settings.DEBUG == True:
    broker_url = 'amqp://'
else:
    broker_url = 'amqp://rabbitmq'

app.conf.broker_url = broker_url 
app.conf.result_backend = 'rpc://'
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['json', 'pickle']
app.conf.result_expires = timedelta(days=1)
app.conf.task_always_eager = False
