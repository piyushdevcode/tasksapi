import os
from celery import Celery

# setting Django setting Module
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')

app = Celery('core')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')
# to configure celery directly from Django settings
app.config_from_object('django.conf:settings',namespace='CELERY')

# loading the task modules from all registered apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')