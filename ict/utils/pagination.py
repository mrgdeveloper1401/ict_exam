from rest_framework import pagination


class CommonPagination(pagination.PageNumberPagination):
    page_size = 20
