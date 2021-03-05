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
        if len(self.content) <= 500:
            return self.content
        try:
            index = self.content[500:].index(' ')
        except (ValueError, Exception):
            index = len(self[500:])
        return f"{self.content[:500+index]}....."


class Comment(models.Model):
    comment = models.TextField(max_length=150)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Blog, on_delete=models.CASCADE)
