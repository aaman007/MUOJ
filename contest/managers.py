from django.db import models
from django.db.models import F, ExpressionWrapper, Q, Count
from django.utils import timezone


class ContestManager(models.Manager):

    def running_contests(self, username=None):
        """
        Returns all running contests of Contest Model
        """

        return super().get_queryset().annotate(
            end_time=ExpressionWrapper(
                F('start_time') + F('duration'),
                output_field=models.DateTimeField()
            ),
            is_registered=Count(
                'contestants',
                filter=(Q(contestants__username=username))
            )
        ).filter(
            start_time__lte=timezone.now(),
            end_time__gte=timezone.now()
        )

    def upcoming_contests(self, username=None):
        """
        Returns all upcoming contests of Contest Model
        """

        return super().get_queryset().filter(
            start_time__gt=timezone.now()
        ).annotate(
            is_registered=Count(
                'contestants',
                filter=(Q(contestants__username=username))
            )
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

    def user_participation(self, user=None):
        """
        Returns all rated contests that a given user participated while the contest was running
        All returned contests are among past contests and rated
        """

        return self.get_queryset().annotate(
            end_time=ExpressionWrapper(
                F('start_time') + F('duration'),
                output_field=models.DateTimeField()
            )
        ).filter(
            end_time__lt=timezone.now(),
            submissions__user=user,
            submissions__created_at__lte=F('end_time'),
            is_rated=True
        )

