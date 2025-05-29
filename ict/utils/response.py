from rest_framework import response, status as res_status


def success_response(message, data=None, status=res_status.HTTP_200_OK):
    return response.Response({
        "success": True,
        "message": message,
        "data": data or {}
    }, status=status)
