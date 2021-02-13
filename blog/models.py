from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import RichTextField

from core.models import AbstractBaseModel


class Blog(AbstractBaseModel):
    title = models.CharField(max_length=100)
    content = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')
        ordering = ['id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def truncated_content(self):
        try:
            index = self.content[500:].index(' ')
            #index = 500
        except (ValueError, Exception):
            index = len(self[500:])
        return self.content if len(self.content) <= 500 else f"{self.content[:500+index]}....."
