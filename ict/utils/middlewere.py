# your_app/middleware.py

from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class APIResponseWrapperMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 200:
            response.data = {
                "success": True,
                "data": response
            }
        response = Response(response).data
        return response
