from time import sleep
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


from .serializers import UserSerializer


@shared_task()
def send_activation_email(url, email):
    send_mail('Verification',url,settings.EMAIL_HOST_USER, [email], fail_silently=False)