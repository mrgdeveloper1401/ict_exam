from rest_framework import urls
from django.urls import path, include
from rest_framework_nested import routers

from . import views

app_name = 'v1_exam'

router = routers.SimpleRouter()
router.register('exam', views.ExamViewSet, basename='exam')

urlpatterns = [

] + router.urls
