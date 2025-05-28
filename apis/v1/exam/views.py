from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from exam_app.models import Exam
from ict.utils.pagination import CommonPagination
from . import serializers


class ExamViewSet(viewsets.ModelViewSet):
    """
    pagination --> 20 items per page
    condition --> if user is admin equal true, can create and deleted and update view
    filter query --> ?title=anything
    """
    queryset = Exam.objects.select_related("creator").only(
        "title",
        "created_at",
        "updated_at",
        "description",
        "time_limit",
        "creator__full_name",
        "is_active"
    )
    serializer_class = serializers.ExamSerializer
    pagination_class = CommonPagination
    filterset_fields = ("title",)
    filter_backends = (DjangoFilterBackend,)

    # if user is admin equal true, can create and deleted and update view
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()
