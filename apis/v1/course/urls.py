from django.urls import path, include
from rest_framework_nested import routers
from .views import CategoryViewSet, CourseViewSet

app_name = 'v1_course'

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

courses_router = routers.NestedDefaultRouter(router, r'categories', lookup='category')
courses_router.register(r'courses', CourseViewSet, basename='category-courses')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(courses_router.urls)),
]
