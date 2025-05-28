from rest_framework import serializers
from course_app.models import Category, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'code', 'description',
            'thumbnail', 'level', 'credit', 'duration',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'category_name', 'category_slug',
            'is_publish', 'created_at', 'updated_at'
        ]
        read_only_fields = ['category_slug',]


class CategoryDetailSerializer(CategorySerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['courses']


class CourseDetailSerializer(CourseSerializer):
    category = CategorySerializer(read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['category']