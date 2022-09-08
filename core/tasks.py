from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# shared task 

@shared_task(bind=True)
def send_mail_to_leader(self,**kwargs):
    """
    send email to leader by specifying the message and subject 
    """
    subject = kwargs['subject']
    message = kwargs['message']
    recepient_list = kwargs['to_email']
    print(f'self is {self} \n kwargs: {kwargs}')
    # send_mail(subject=subject,
    #           message=message,
    #           from_email=settings.EMAIL_HOST_USER,
    #           recipient_list=[recepient_list],
    #           fail_silently=False,
    #             )
    return kwargs['onsuccess']