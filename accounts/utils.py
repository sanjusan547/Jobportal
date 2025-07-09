from django.core.mail import send_mail
from django.conf import settings

def send_notification_mail(subject,message,to_email):
    send_mail(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Uses DEFAULT_FROM_EMAIL
        recipient_list=[to_email],
        fail_silently=False,

    )
