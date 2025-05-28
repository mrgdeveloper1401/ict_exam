from django.db import models
from django.utils import timezone


class SoftQuerySet(models.QuerySet):
    def delete(self):
        return super().update(
            is_deleted=True,
            deleted_at=timezone.now()
        )


class SoftManager(models.Manager):
    def get_queryset(self):
        return SoftQuerySet(self.model, using=self._db).filter(
            models.Q(is_deleted=None) | models.Q(is_deleted=False), deleted_at=None
        )
