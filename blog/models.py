from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from core.models import AbstractBaseModel

User = get_user_model()


User = get_user_model()


class Blog(AbstractBaseModel):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    content = RichTextField(verbose_name=_('Content'))
    user = models.ForeignKey(verbose_name=_('User'), to=User, on_delete=models.CASCADE)
    preference = models.BooleanField(verbose_name=_('Preference'), default=False)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def truncated_content(self):
        if len(self.content) <= 500:
            return self.content
        try:
            index = self.content[500:].index(' ')
        except (ValueError, Exception):
            index = len(self[500:])
        return f"{self.content[:500+index]}....."


class Comment(models.Model):
    comment = models.TextField(verbose_name=_('Comment'), max_length=150)
    date_posted = models.DateTimeField(verbose_name=_('Date Posted'), auto_now_add=True)
    date_modified = models.DateTimeField(verbose_name=_('Date Modified'), auto_now=True)
    author = models.ForeignKey(verbose_name=_('Author'), to=User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(verbose_name=_('Post'), to=Blog, on_delete=models.CASCADE)
