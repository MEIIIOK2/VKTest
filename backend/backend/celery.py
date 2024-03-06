import os
import time
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

celery = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.conf.broker_url = settings.CELERY_BROKER_URL
# Load task modules from all registered Django apps.
celery.autodiscover_tasks()


@celery.task(bind=True, ignore_result=True)
def debug_task(self):
    time.sleep(10)
    print('Hi!')