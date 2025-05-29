from django.urls import path, include
from rest_framework_nested import routers

from . import views

app_name = 'v1_exam'

router = routers.SimpleRouter()
router.register('exam', views.ExamViewSet, basename='exam')
router.register("user_answer", views.UserAnswerViewSet, basename='user_answer')

exam_router = routers.NestedSimpleRouter(router, r'exam', lookup='exam')
exam_router.register('questions', views.QuestionViewSet, basename='exam-questions')
exam_router.register('exam_attempts', views.ExamAttemptViewSet, basename='exam_attempts')

urlpatterns = [
    path('', include(exam_router.urls)),
] + router.urls
