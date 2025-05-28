from rest_framework import exceptions


class CustomValidationError(exceptions.APIException):
    status_code = 400

    def __init__(self, detail, code=None):
        super().__init__(detail=detail, code=code)
