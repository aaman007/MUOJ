from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

from core.models import AbstractBaseModel
from contest.managers import ContestQuerySet


User = get_user_model()


class Contest(AbstractBaseModel):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    description = RichTextField(verbose_name=_('Description'))
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    duration = models.DurationField(verbose_name=_('Duration'))

    openness = models.BooleanField(verbose_name=_('Openness'), default=False)
    is_rated = models.BooleanField(verbose_name=_('Is Rated'), default=False)
    rating_applied = models.BooleanField(verbose_name=_('Rating Applied?'), default=False)

    problem_ids = models.JSONField(verbose_name=_('Problem Ids'), default=list)
    problem_scores = models.JSONField(verbose_name=_('Problem Scores'), default=list)
    """
    Standings Format
    [
        {
            'id': 23,
            'username': 'Farhan_Meb',
            'rank': 1400,
            'total_score': 300,
            'scores_per_problem': [100, 200]
        },
        {
            'id': 24,
            'username': 'Decayed',
            'rank': 1200,
            'total_score': 200,
            'scores_per_problem': [0, 200]
        }
    ]
    """
    standings = models.JSONField(verbose_name=_('Standings'), default=list, blank=True)

    author = models.ForeignKey(
        verbose_name=_('Author'),
        to=User,
        related_name='contests',
        on_delete=models.SET_NULL,
        null=True
    )
    contestants = models.ManyToManyField(
        verbose_name=_('Contestants'),
        to=User,
        related_name='contestants',
        blank=True
    )

    objects = ContestQuerySet.as_manager()

    class Meta:
        verbose_name = _('Contest')
        verbose_name_plural = _('Contests')
        ordering = ['-id']

    def __str__(self):
        return self.title

    @property
    def state(self):
        if self in Contest.objects.running_contests():
            return 'Running'
        elif self in Contest.objects.past_contests():
            return 'Finished'
        return 'Upcoming'


class Announcement(AbstractBaseModel):
    title = models.CharField(verbose_name=_('Title'), max_length=200, default='')
    content = models.TextField(verbose_name=_('Content'), default='')

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

    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
        ordering = ['-id']

    def __str__(self):
        return self.title


