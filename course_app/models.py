from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from treebeard.mp_tree import MP_Node

from core_app.models import ModifyMixin, SoftDeleteMixin


class Category(MP_Node, ModifyMixin, SoftDeleteMixin):
    category_name = models.CharField(max_length=255, help_text=_("نام دسته بندی"))
    category_slug = models.SlugField(max_length=255, allow_unicode=True, help_text=_("اسلاگ دسته بندی"), blank=True)
    is_publish = models.BooleanField(default=True, help_text=_("فعال"))

    def __str__(self):
        return self.category_name

    node_order_by = ("category_name",)

    def save(self, *args, **kwargs):
        self.category_slug = slugify(self.category_name, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "category_course"
        ordering = ('created_at',)


class Course(MP_Node, ModifyMixin, SoftDeleteMixin):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='course',
    )
    class CourseLevel(models.TextChoices):
        BASIC = 'basic', 'مبتدی'
        INTERMEDIATE = 'intermediate', 'متوسط'
        ADVANCED = 'advanced', 'پیشرفته'

    # information course
    title = models.CharField(max_length=100, help_text=_('عنوان درس'))
    slug = models.SlugField(max_length=255, help_text=_('شناسه URL'), allow_unicode=True, blank=True)
    code = models.CharField(
        max_length=20,
        unique=True,
        help_text=_('کد درس'),
        validators=[MinLengthValidator(3)]
    )
    description = models.TextField(help_text=_('توضیحات درس'))
    # thumbnail = models.ForeignKey("core_app.Image", help_text=_('تصویر درس'), on_delete=models.PROTECT)
    thumbnail = models.ImageField(upload_to="course/%Y/%m/%d", blank=True, null=True, help_text=_("تصویر درس"))

    # Technical specifications
    level = models.CharField(
        max_length=20,
        choices=CourseLevel.choices,
        default=CourseLevel.BASIC,
        help_text=_('سطح درس')
    )
    credit = models.PositiveSmallIntegerField(default=1, help_text=_('واحد درس'))
    duration = models.DurationField(help_text=_('مدت زمان دوره'))
    is_active = models.BooleanField(default=True, help_text=_('فعال'))


    class Meta:
        db_table = 'course'
        ordering = ('created_at',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)
