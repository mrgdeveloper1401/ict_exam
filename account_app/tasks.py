from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


# task celery send email
@shared_task
def send_reset_password_code(to_email, subject, message):
    from_email = settings.EMAIL_HOST_USER
    receiver_email = to_email
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[receiver_email],
        fail_silently=True
    )
