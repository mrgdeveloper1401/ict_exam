from django.contrib.auth.models import BaseUserManager
from django.db import models

from core_app.manager import SoftQuerySet


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('mobile phone number required')

        user = self.model(
            phone_number=phone_number,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # we dont use password
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # بررسی فیلدهای الزامی برای سوپر یوزر
        required_fields = ('email', 'nation_code', 'full_name')
        for field in required_fields:
            if field not in extra_fields:
                raise ValueError(f'{field} is required')

        return self.create_user(phone_number, password, **extra_fields)

    def get_queryset(self):
        return SoftQuerySet(self.model, using=self._db).filter(
            models.Q(is_deleted=None) | models.Q(is_deleted=False), deleted_at=None
        )
