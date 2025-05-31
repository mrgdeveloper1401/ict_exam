from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

from . import views

app_name = "v1_auth"

router = routers.SimpleRouter()

router.register(r'signup', views.UserRegisterViewSet, basename='user')
router.register(r'profile', views.StudentProfileViewSet, basename='student_profile')

urlpatterns = [
    path("", include(router.urls)),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("rest_password/", views.ResetPasswordView.as_view(), name="password_reset"),
    path("send_email_to_user/", views.AdminSendEmailView.as_view(), name="send_email_to_user"),
]
