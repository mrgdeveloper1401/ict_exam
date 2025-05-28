from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, views, response, generics

from account_app.models import User
# from ict.utils.pagination import CommonPagination
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
