from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, exceptions

from exam_app.models import Exam, Question, ExamAttempt, Option, UserAnswer
from ict.utils.pagination import CommonPagination
from . import serializers


class ExamViewSet(viewsets.ModelViewSet):
    """
    pagination --> 20 items per page
    condition --> if user is admin equal true, can create and deleted and update view
    filter query --> ?title=anything
    """
    serializer_class = serializers.ExamSerializer
    pagination_class = CommonPagination

    # if user is admin equal true, can create and deleted and update view
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            self.permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        else:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()

    def filter_queryset(self, queryset):
        title = self.request.query_params.get("title", None)

        if title:
            queryset = queryset.filter(title__icontains=title)
        return queryset

    def get_queryset(self):
        query = Exam.objects.select_related("creator").only(
            "title",
            "created_at",
            "updated_at",
            "description",
            "time_limit",
            "creator__full_name",
            "is_active",
            "exam_image"
        )
        if self.request.user.is_staff is False:
                query.filter(is_active=True)
        return query


class QuestionViewSet(viewsets.ModelViewSet):
    """
    for method post and update and delete --> only admin user \n
    for method get user must create exam_attempts
    """
    serializer_class = serializers.QuestionSerializer

    # if user is admin equal true, can create and deleted and update view
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (permissions.IsAdminUser,)
        return super().get_permissions()

    def get_queryset(self):
        query = Question.objects.filter(
            exam_id=self.kwargs["exam_pk"],
        ).defer(
            "is_deleted",
            "deleted_at",
        )

        if self.request.user.is_staff is False:
            query = query.filter(is_active=True)
        return query

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['exam_pk'] = self.kwargs['exam_pk']
        return context

    def check_exam_attempt_permission(self, request):
        """check permission ExamAttempt"""
        get_exam_attempt = ExamAttempt.objects.filter(
            user_id=request.user.id,
            exam_id=self.kwargs.get("exam_pk"),
            ip_address=request.META.get("REMOTE_ADDR", "X_FORWARDED_FOR"),
        ).select_related("exam").only("exam__title")

        if not get_exam_attempt.exists():
            raise exceptions.PermissionDenied()

    def list(self, request, *args, **kwargs):
        self.check_exam_attempt_permission(request)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.check_exam_attempt_permission(request)
        return super().retrieve(request, *args, **kwargs)


class ExamAttemptViewSet(viewsets.ModelViewSet):
    """
    Registration for the relevant exam \n
    To access the questions, the user must first send a post request to access the questions.
    """
    serializer_class = serializers.ExamAttemptSerializer
    pagination_class = CommonPagination

    def get_queryset(self):
        return ExamAttempt.objects.defer(
        "is_deleted", "deleted_at"
    ).filter(
            exam_id=self.kwargs["exam_pk"],
            user_id=self.request.user.id,
        )

    # just only admin user can update and delete question
    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", 'DELETE'):
            self.permission_classes = (permissions.IsAdminUser,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # get exam id of url_params
        context['exam_pk'] = self.kwargs.get('exam_pk')
        return context


class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OptionSerializer
    queryset = Option.objects.defer("is_deleted", "deleted_at")
    permission_classes = (permissions.IsAuthenticated,)


class UserAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserAnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return UserAnswer.objects.filter(attempt__user=self.request.user).defer("is_deleted", "deleted_at")
