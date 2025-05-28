from rest_framework import routers
from django.urls import path, include


from . import views

app_name = "v1_auth"

router = routers.SimpleRouter()

router.register(r'signup', views.UserRegisterViewSet, basename='user')
router.register(r'profile', views.StudentProfileViewSet, basename='student_profile')

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.UserLoginView.as_view(), name="login"),
    # path("request_otp_phone/", views.RequestOtpView.as_view(), name="request_otp_phone"),
    # path("request_otp_verify/", views.RequestOtpVerifyView.as_view(), name="request_otp_verify"),
    path('auth/password/reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('auth/password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
