import os
from celery import Celery
from celery.schedules import crontab
# setting Django setting Module
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')

app = Celery('core')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Kolkata')
# to configure celery directly from Django settings
app.config_from_object('django.conf:settings',namespace='CELERY')

# loading the task modules from all registered apps
app.autodiscover_tasks()

# for testing 
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# TESTING CELERY BEAT 
app.conf.beat_schedule = {
    'send-mail-task-crontab' :{
    'task': 'send_mail_to_leader',
    'schedule': crontab(hour=19,minute=46),
    'kwargs' :{'subject':'Celery beat Testing','to_email':'piyushdevliyal25@gmail.com',
    'message':'Test message',
    'onsuccess':'Done'}
    },
}