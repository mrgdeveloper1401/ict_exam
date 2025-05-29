from django.db import models
from django.db.models import Q

from core_app.models import ModifyMixin, SoftDeleteMixin, UpdateMixin, CreateMixin
from django.utils.translation import gettext_lazy as _

from exam_app.enums import AnswerEnums


class Exam(ModifyMixin, SoftDeleteMixin):
    """
    exam model
    """
    title = models.CharField(
        max_length=200,
        help_text=_("عنوان ازمون")
    )
    description = models.TextField(
        blank=True,
        help_text=_("توضیح ازمون")
    )
    creator = models.ForeignKey(
        "account_app.User",
        on_delete=models.PROTECT,
        related_name="exam_creator",
        help_text=_("ایجاد کننده"),
        limit_choices_to=(Q(is_staff=True) | Q(user_type="teacher") & Q(is_active=True))
    )
    time_limit = models.PositiveIntegerField(
        help_text=_("مدت زمان")
    )
    exam_type = models.CharField(
        help_text=_("نوع سوال"),
        max_length=20,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_("فعال")
    )
    exam_image = models.ImageField(
        upload_to="exam_images/%Y/%m/%d",
        blank=True,
        null=True,
        help_text=_("کاور ازمون")
    )

    class Meta:
        db_table = "exam"
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Question(ModifyMixin, SoftDeleteMixin):
    """
    question model
    """
    exam = models.ForeignKey(
        Exam,
        on_delete=models.PROTECT,
        related_name='questions',
        help_text=_("Exam that this question belongs to")
    )
    text = models.TextField(
        help_text=_("Full text of the question")
    )
    is_active = models.BooleanField(default=True, help_text=_("فعال"))

    class Meta:
        db_table = "question"
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.exam.title}"


class Option(ModifyMixin, SoftDeleteMixin):
    """
    option model
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name='options',
        help_text=_("سوال")
    )
    text = models.CharField(
        max_length=500,
        help_text=_("جواب سوال")
    )
    is_correct = models.BooleanField(
        default=False,
        help_text=_("ایا صحیح هست یا خیر")
    )

    class Meta:
        db_table = "option"
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.question.text[:30]} {self.is_correct}'


class ExamAttempt(ModifyMixin, SoftDeleteMixin):
    """
    Exam attempt model
    """
    user = models.ForeignKey(
        "account_app.User",
        on_delete=models.CASCADE,
        related_name='exam_attempts',
        help_text=_("کاربر")
    )
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='attempts',
        help_text=_("ازمون")
    )
    start_time = models.DateTimeField(
        auto_now_add=True,
        help_text=_("زمان شروع")
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("زمان پایان که کاربر پایان ازمون رو زده هست")
    )
    score = models.FloatField(
        null=True,
        blank=True,
        help_text=_("نمره")
    )
    ip_address = models.GenericIPAddressField(
        help_text=_("ادرس ای پی کاربر")
    )
    result_color = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        help_text=_("نتیجه ازمون به صورت وضعیت رنگی")
    )

    class Meta:
        db_table = "exam_attempt"
        ordering = ('-start_time',)

    def __str__(self):
        return f"{self.exam.title}"


class UserAnswer(CreateMixin, UpdateMixin, SoftDeleteMixin):
    """
    User answer model
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        help_text=_("سوال"),
        related_name='question_user_answers',
    )
    answer = models.CharField(
        help_text=_("پاسخ"),
        choices=AnswerEnums.choices,
        # TODO, clean migrations
        blank=True,
    )

    class Meta:
        db_table = "user_answer"
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.question.exam.title} {self.answer} {self.created_at}"
