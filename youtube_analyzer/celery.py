from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_analyzer.settings')

app = Celery('youtube_analyzer')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'amqp://guest:guest@rabbitmq_server:5672//'

app.autodiscover_tasks()