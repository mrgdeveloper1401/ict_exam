from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

from core_app.models import ModifyMixin, SoftDeleteMixin, UpdateMixin
from django.utils.translation import gettext_lazy as _


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
    # passing_score = models.PositiveIntegerField(
    #     help_text=_("نمره قبولی"),
    #     validators=[MinValueValidator(0), MaxValueValidator(100)]
    # )
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
    # image = models.ForeignKey(
    #     "core_app.Image",
    #     on_delete=models.PROTECT,
    #     help_text=_("Optional image related to the question"),
    #     null=True,
    #     blank=True
    # )
    # score = models.PositiveIntegerField(
    #     default=1,
    #     validators=[MinValueValidator(1)],
    #     help_text=_("Points awarded for correct answer to this question")
    # )

    class Meta:
        db_table = "question"

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
    # is_passed = models.BooleanField(
    #     default=False,
    #     help_text=_("Did the user pass this attempt?")
    # )
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


class UserAnswer(UpdateMixin, SoftDeleteMixin):
    """
    User answer model
    """
    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.PROTECT,
        related_name='user_answers',
        help_text=_("شرکت در ازمون")
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        help_text=_("سوال")
    )
    option = models.ForeignKey(
        Option,
        on_delete=models.PROTECT,
        help_text=_("جواب")
    )
    answered_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("زمان پاسخ")
    )

    class Meta:
        db_table = "user_answer"
        unique_together = ('attempt', 'question')

    def __str__(self):
        return self.attempt.user.phone_number
