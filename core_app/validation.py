from django.conf import settings
from django.core import exceptions


def validate_image_size(value):
    # get max size on settings
    max_size = settings.IMAGE_SIZE_MAX

    # max image size
    image_size = value.size / 1024 / 1024

    # check image size
    if max_size > value.size:
        raise exceptions.ValidationError(
            message=f"max size image is {max_size} MB, you image size is {image_size:2f}",
            code="max_size"
        )
    return value
