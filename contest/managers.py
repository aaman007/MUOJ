from django.db import models
from django.db.models import F, ExpressionWrapper, Q, Count
from django.utils import timezone


class ContestQuerySet(models.QuerySet):

    def running_contests(self, username=None):
        """
        Returns all running contests of Contest Model
        """

        return self.annotate(
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
        ).order_by('-start_time')

    def upcoming_contests(self, username=None):
        """
        Returns all upcoming contests of Contest Model
        """

        return self.filter(
            start_time__gt=timezone.now()
        ).annotate(
            is_registered=Count(
                'contestants',
                filter=(Q(contestants__username=username))
            )
        ).order_by('-start_time')

    def past_contests(self):
        """
        Returns all past contests of Contest Model
        """

        return self.annotate(
            end_time=ExpressionWrapper(
                F('start_time') + F('duration'),
                output_field=models.DateTimeField()
            )
        ).filter(
            end_time__lt=timezone.now()
        ).order_by('-start_time')

    def user_participation(self, user=None):
        """
        Returns all rated contests that a given user participated while the contest was running
        All returned contests are among past contests and rated
        """

        return self.annotate(
            end_time=ExpressionWrapper(
                F('start_time') + F('duration'),
                output_field=models.DateTimeField()
            )
        ).filter(
            end_time__lt=timezone.now(),
            submissions__user=user,
            submissions__created_at__lte=F('end_time'),
            is_rated=True
        ).order_by('-start_time')
