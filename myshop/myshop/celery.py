import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

# All Celery settings will have prefix "CELERY_"
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover asynchronous tasks.  They'll be in a 'tasks.py' file in the
# root of each application.
app.autodiscover_tasks()
