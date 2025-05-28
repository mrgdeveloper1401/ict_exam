from rest_framework import routers
from django.urls import path, include


from . import views

app_name = "v1_auth"

router = routers.DefaultRouter()

router.register(r'signup', views.UserRegisterViewSet, basename='user')
# router.register("profile", views.UserProfileViewSet, basename='profile')

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.UserLoginView.as_view(), name="login"),
    # path("request_otp_phone/", views.RequestOtpView.as_view(), name="request_otp_phone"),
    # path("request_otp_verify/", views.RequestOtpVerifyView.as_view(), name="request_otp_verify"),
    # path("change_password/"),
    # path("change_password_confirm/"),
]