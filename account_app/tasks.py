from celery import shared_task
from decouple import config
from django.core.mail import send_mail


@shared_task
def send_reset_password_code(to_email, code):
    subject = "request password reset"
    message = f"you otp code is {code}"
    from_email = config('DEFAULT_FROM_EMAIL', cast=str)
    receiver_email = to_email
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[receiver_email],
    )
