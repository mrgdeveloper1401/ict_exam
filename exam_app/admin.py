from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    raw_id_fields = ("creator",)
    list_display = ("title", "creator", "time_limit", "created_at", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    date_hierarchy = "created_at"
    search_help_text = _("برای سرچ از عنوان ازمون استفاده کنید")
    list_select_related = ("creator",)
    list_per_page = 20
    list_editable = ("is_active",)

    def get_queryset(self, request):
        return super().get_queryset(request).only(
            "creator__phone_number",
            "title",
            "time_limit",
            "created_at",
            "is_active",
            "description",
            "exam_image",
            # "exam_start_time"
        )


@admin.register(models.UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    raw_id_fields = ("question", "option")
    list_display = ("question", "option", "answer", "created_at",)
    list_editable = ("answer",)
    search_fields = ("question__exam__title",)
    search_help_text = _("برای جست و جو میتوانید از عنوان ازمون استفاده کنید")
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "question__exam",
            "option"
        ).only(
            "answer",
            "question__exam__title",
            "question__text",
            "created_at",
            "option__question__text",
        )


@admin.register(models.ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "exam")
    list_display = ("user", "exam", "end_time", "score", "ip_address", "result_color")
    list_per_page = 30
    list_filter = ("created_at",)
    search_fields = ("user__phone_number",)
    search_help_text = _("برای جست و جو میتواندی از شماره موبایل کاربر استفاده کیند")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "user", "exam"
        ).only(
            "user__phone_number",
            "exam__title",
            "end_time",
            "score",
            "ip_address",
            "result_color"
        )


@admin.register(models.Option)
class OptionAdmin(admin.ModelAdmin):
    raw_id_fields = ("question",)
    list_display = ("question", "created_at")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    list_per_page = 30

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "question__exam"
        ).only(
            "created_at",
            "question__exam__title",
        )


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    raw_id_fields = ('exam',)
    list_display = ("exam", "created_at", "is_active")
    list_editable = ("is_active",)
    list_per_page = 20
    search_fields = ("exam__title",)
    list_filter = ("is_active",)
    search_help_text = _("برای سرچ کردن از عنوان ازمون یا exam استفاده کنید")
    date_hierarchy = "created_at"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("exam").only(
            "exam__title",
            "created_at",
            "is_active",
            "text"
        )
