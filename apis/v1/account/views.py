from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, views, response, status, permissions
import random

from account_app.models import User, Student
from . import serializers
from .permissions import NotAuthenticated
from .serializers import TokenResponseSerializer


class UserRegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    condition --> you can only send phone_number and password for create user, full_name and email can not require
    """
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (NotAuthenticated,)

    @extend_schema(
        responses=serializers.CreateResponseSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class UserLoginView(views.APIView):
    """
    login by phone number and password
    """
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (NotAuthenticated,)

    @extend_schema(
        responses=TokenResponseSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # get token after validated data
        token = serializer.validated_data['token']
        role = serializer.validated_data['tole']
        is_staff = serializer.validated_data['is_staff']
        return response.Response(
            {
                'token': token,
                "is_staff": is_staff,
                "role": role,
                "success": True,
            }
        )


class StudentProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = serializers.StudentProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Student.objects.select_related("user").filter(
            user=self.request.user
        ).only(
            "user__full_name",
            "user__email",
            "user__nation_code",
            "user__phone_number",
            "user__user_type",
            "student_number",
            "student_image",
            "grade",
            "parent_phone"
        )
