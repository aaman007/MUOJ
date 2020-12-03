from django.db import models
from django.db.models import F, ExpressionWrapper
from django.utils import timezone


class ContestManager(models.Manager):

    def running_contests(self):
        """
        Returns all running contests of Contest Model
        """

        return super().get_queryset().annotate(
            end_time=ExpressionWrapper(
                F('start_time') + F('duration'),
                output_field=models.DateTimeField()
            )
        ).filter(
            start_time__lte=timezone.now(),
            end_time__gte=timezone.now()
        )

    def upcoming_contests(self):
        """
        Returns all upcoming contests of Contest Model
        """

        return super().get_queryset().filter(
            start_time__gt=timezone.now()
        )

    def past_contests(self):
        """
        Returns all past contests of Contest Model
        """

        return super().get_queryset().annotate(
            end_time=ExpressionWrapper(
                F('start_time') + F('duration'),
                output_field=models.DateTimeField()
            )
        ).filter(
            end_time__lt=timezone.now()
        )
