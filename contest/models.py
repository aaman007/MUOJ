from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from core.models import AbstractBaseModel


User = get_user_model()


class Contest(AbstractBaseModel):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    duration = models.DurationField(verbose_name=_('Duration'))

    openness = models.BooleanField(verbose_name=_('Openness'), default=False)
    is_rated = models.BooleanField(verbose_name=_('Is Rated'), default=False)

    problem_ids = models.JSONField(verbose_name=_('Problem Ids'), default=list)
    problem_scores = models.JSONField(verbose_name=_('Problem Scores'), default=list)

    author = models.ForeignKey(
        verbose_name=_('Author'),
        to=User,
        related_name='contests',
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.title


class Announcement(AbstractBaseModel):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    content = models.TextField(verbose_name=_('Content'))

    user = models.ForeignKey(
        verbose_name=_('User'),
        to=User,
        related_name='announcements',
        on_delete=models.CASCADE
    )
    contest = models.ForeignKey(
        verbose_name=_('Contest'),
        to=Contest,
        related_name='announcements',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Clarification(AbstractBaseModel):
    content = models.TextField(verbose_name=_('Content'))

    user = models.ForeignKey(
        verbose_name=_('User'),
        to=User,
        related_name='clarifications',
        on_delete=models.CASCADE
    )
    contest = models.ForeignKey(
        verbose_name=_('Contest'),
        to=Contest,
        related_name='clarifications',
        on_delete=models.CASCADE
    )
    problem_id = models.PositiveIntegerField(verbose_name=_('Problem Id'))
