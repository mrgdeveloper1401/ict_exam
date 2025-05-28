from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from . import models


@receiver(post_save, sender=models.User)
def create_student(sender, instance, created, **kwargs):
    year = timezone.now().year
    if created:
        models.Student.objects.create(
            user=instance,
            student_number=f"s{year}{instance.id}"
        )
