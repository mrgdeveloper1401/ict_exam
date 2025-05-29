from axes.handlers.proxy import AxesProxyHandler
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, views, response, permissions, exceptions

from account_app.models import User, Student, UserLoginLogs
from . import serializers
from .exceptions import CustomValidationError
from .permissions import NotAuthenticated
from .serializers import TokenResponseSerializer
from .token import get_tokens_for_user


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
    if user wrong password and phone he block until 10 minute
    """
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (NotAuthenticated,)

    @extend_schema(responses=TokenResponseSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        password = serializer.validated_data['password']

        user = authenticate(
            request=request,
            phone_number=phone_number,
            password=password,
        )

        #  check axes
        # if AxesProxyHandler.is_locked(request):
        #     raise exceptions.PermissionDenied("Too many failed login attempts. Try again later.")

        if not user:
            raise CustomValidationError({
                "message": "phone and password is invalid",
                "success": False
            })

        # create token
        token = get_tokens_for_user(user)
        role = user.user_type
        is_staff = user.is_staff

        # save information log
        UserLoginLogs.objects.create(
            user=user,
            device_ip=request.META.get('REMOTE_ADDR', request.META.get('HTTP_X_FORWARDED_FOR', '')),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )

        return response.Response({
            'token': token,
            'is_staff': is_staff,
            'role': role,
            'success': True,
        })


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
