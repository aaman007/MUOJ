from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Constant(models.Model):
    key = models.CharField(verbose_name=_('Key'), max_length=255)
    value = models.CharField(verbose_name=_('Value'), max_length=255)
    remote = models.BooleanField(verbose_name=_('Remote'), default=False)

    def __str__(self):
        return self.key
