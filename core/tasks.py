from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# shared task 

@shared_task(bind=True)
def send_mail_to_leader(self,**kwargs):

    send_mail(subject="New task",
              message="new msg",
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=['piyushdevcode@gmail.com'],
              fail_silently=True,
                )
    print(f'self is {self} \n kwargs: {kwargs}')
    return kwargs['onsuccess']