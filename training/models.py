from django.db import models
from django.utils.translation import gettext_lazy as _


class Tutorial(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    tutorial = models.TextField(verbose_name=_('Description'), blank=True)
    problem_ids = models.JSONField(verbose_name=_('Problem Ids'), default=list)
    level = models.PositiveIntegerField(verbose_name=_('Level'), unique=True, default=1)

    def __str__(self):
        return self.title
