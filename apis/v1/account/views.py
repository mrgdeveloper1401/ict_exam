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


# class RequestOtpView(generics.CreateAPIView):
#     serializer_class = serializers.RequestOtpSerializer
#     permission_classes = (NotAuthenticated,)
#     queryset = User.objects.only(
#         "phone_number"
#     )


# class RequestOtpVerifyView(views.APIView):
#     serializer_class = serializers.RequestVerifyOtpSerializer
#     permission_classes = (NotAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         token = serializer.validated_data['token']
#         return response.Response(token)


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


class PasswordResetRequestView(views.APIView):
    serializer_class = serializers.PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # تولید کد تأیید (مثلاً 4 رقمی)
            verification_code = str(random.randint(1000, 9999))

            # ذخیره کد در کش به مدت 5 دقیقه
            cache.set(f'password_reset_{phone_number}', verification_code, 300)

            # در اینجا باید کد را به کاربر ارسال کنید (با SMS یا ایمیل)
            # این بخش بستگی به سرویس SMS شما دارد
            # send_sms(phone_number, f'کد تأیید شما: {verification_code}')

            return response.Response({
                'message': 'کد تأیید به شماره تلفن شما ارسال شد.',
                'phone_number': phone_number,
                'expires_in': '5 دقیقه'
            }, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(views.APIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(phone_number=phone_number)
                user.set_password(new_password)
                user.save()

                # پاک کردن کد از کش
                cache.delete(f'password_reset_{phone_number}')

                return response.Response({
                    'message': 'رمز عبور با موفقیت تغییر یافت.'
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return response.Response({
                    'error': 'کاربر یافت نشد.'
                }, status=status.HTTP_404_NOT_FOUND)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        del request.auth.token
        return response.Response(status=status.HTTP_204_NO_CONTENT)
