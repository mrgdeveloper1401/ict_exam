from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models
# Register your models here.


@admin.register(models.Otp)
class OtpAdmin(admin.ModelAdmin):
    list_per_page = 30
    list_display = ("phone_number", "otp_code", "device_ip", "created_at", "is_expired", "expired_otp")
    search_fields = ("phone_number",)
    search_help_text = _("برای جست و جو میتوانید از شماره موبایل استفاده کنید")


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("full_name", "email", "user_type")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )
    list_editable = ("user_type",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "user_type", "usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("phone_number", "email", "full_name", "user_type", "is_staff", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("phone_number", "full_name", "email")
    ordering = ("-created_at",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ("created_at", "updated_at", "last_login")


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "student_image")
    list_display = ("user", "student_number", "grade", "parent_phone", "created_at")
    list_per_page = 30
    search_fields = ("user__phone_number",)
    search_help_text = _("برای جست و جو میتوانید از شماره موبایل استفاده کنید")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "user"
        ).only(
            "user__phone_number",
            "student_number",
            "grade",
            "parent_phone",
            "created_at"
        )