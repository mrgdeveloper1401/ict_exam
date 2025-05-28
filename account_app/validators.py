from rest_framework import exceptions
from django.core.validators import RegexValidator


def unique_email_in_layer_app(value):
    from account_app.models import User

    all_mail = User.objects.filter(
        email=value
    )

    if all_mail.exists():
        raise exceptions.ValidationError(detail="This email is already registered.", code="unique_validator")
    return value


def unique_nation_code_in_layer_app(value):
    from account_app.models import User

    nation_code = User.objects.filter(
        nation_code=value
    )

    if nation_code.exists():
        raise exceptions.ValidationError(detail="This nation_code is already registered.", code="unique_validator")
    return value


class PhoneNumberValidator(RegexValidator):
    regex = r'^\d{9,15}'
    message = "you must valid phone"
    code = 'invalid_phone'
