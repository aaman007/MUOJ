from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.models import AbstractBaseModel

User = get_user_model()


class Channel(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=150, unique=True)
    members = models.ManyToManyField(
        to=User,
        verbose_name=_('Members'),
        related_name='channels'
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('Channel')
        verbose_name_plural = _('Channels')

    def __str__(self):
        return self.title


class Message(AbstractBaseModel):
    text = models.CharField(verbose_name=_('Text'), max_length=500)
    channel = models.ForeignKey(
        to='Channel',
        verbose_name=_('Channel'),
        related_name='messages',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to=User,
        verbose_name=_('User'),
        related_name=_('Messages'),
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ['-id']
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')

    def __str__(self):
        return self.text
