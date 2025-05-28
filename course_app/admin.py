from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from django.utils.translation import gettext_lazy as _

from .models import Category, Course


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ('category_name', 'category_slug', 'is_publish', 'created_at', "updated_at")
    list_filter = ('is_publish', 'created_at')
    search_fields = ('category_name', 'category_slug')
    prepopulated_fields = {'category_slug': ('category_name',)}
    search_help_text = _("برای جست و جو از نام دسته بندی استفاده کنید")

    fieldsets = (
        (None, {
            'fields': ('category_name', 'category_slug', 'is_publish')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).defer(
            "is_deleted",
            "deleted_at"
        )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'credit', 'is_active')
    list_filter = ('category', 'level', 'is_active', 'created_at')
    search_fields = ('title', 'code', 'description')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category', 'thumbnail')
    autocomplete_fields = ('category',)
    list_select_related = ("category",)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'code', 'description', 'category', 'thumbnail')
        }),
        ('Course Details', {
            'fields': ('level', 'credit', 'duration', 'is_active')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "title",
            "category__category_name",
            "slug",
            "code",
            "description",
            "thumbnail",
            "level",
            "credit",
            "duration",
            "is_active"
        )
