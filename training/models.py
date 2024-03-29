from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

from core.models import AbstractBaseModel


class Tutorial(AbstractBaseModel):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    content = RichTextField(verbose_name=_('Description'), blank=True)
    problem_ids = models.JSONField(verbose_name=_('Problem Ids'), default=list)
    level = models.PositiveIntegerField(verbose_name=_('Level'), unique=True, default=1)

    class Meta:
        verbose_name = _('Tutorial')
        verbose_name_plural = _('Tutorials')
        ordering = ['id']

    def __str__(self):
        return self.title

    @property
    def truncated_content(self):
        if len(self.content) < 250:
            return self.content
        return self.content[:250] + "......."
