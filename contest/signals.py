from django.db.models.signals import post_save
from django.dispatch import receiver

from problemset.judge import compile_submission
from problemset.models import Submission


@receiver(post_save, sender=Submission)
def compile_solution(sender, instance, created, **kwargs):
    if created:
        compile_submission(instance)
