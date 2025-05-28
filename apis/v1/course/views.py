from rest_framework import viewsets
from course_app.models import Category, Course
from .serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
    CourseSerializer,
    CourseDetailSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return super().get_serializer_class()


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if 'category_pk' in self.kwargs:
            return Course.objects.filter(category_id=self.kwargs['category_pk'])
        return Course.objects.all()