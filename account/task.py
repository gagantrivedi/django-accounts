import os
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_welcome_mail(username, email_id):
    send_mail('Welcome', 'welcome' + username, os.environ['USER_EMAIL'], [email_id])
    return True
