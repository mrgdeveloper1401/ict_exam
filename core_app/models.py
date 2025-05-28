from django.utils import timezone

from django.db import models

from core_app.manager import SoftManager
from core_app.validation import validate_image_size


class ModifyMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=None, editable=False, null=True)
    deleted_at = models.DateTimeField(default=None, editable=False, null=True)

    class Meta:
        abstract = True

    objects = SoftManager()

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class CreateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# class Image(ModifyMixin, SoftDeleteMixin):
#     title = models.CharField(max_length=128, null=True, blank=True)
#     image = models.ImageField(width_field="width", height_field="height", upload_to="images/%Y/%m/%d",
#                               validators=(validate_image_size,),
#                               help_text="max size is 2 MG")
#     width = models.IntegerField(null=True, blank=True)
#     height = models.IntegerField(null=True, blank=True)
#     file_size = models.PositiveIntegerField(null=True, blank=True, help_text="file size as xx.b")

    # @property
    # def image_url(self):
        # show url image
        # return self.image.url if self.image else None

    # def save(self, *args, **kwargs):
        # save image size
        # self.file_size = self.image.size
        # return super().save(*args, **kwargs)

    # class Meta:
    #     db_table = "image"
    #     verbose_name = "Image"
    #     verbose_name_plural = "Images"
    #     ordering = ('-created_at',)
