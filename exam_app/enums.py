from django.db import models


class AnswerEnums(models.TextChoices):
    A = "a",
    B = "b",
    C = "c",
    D = "d",
