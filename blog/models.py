from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def truncated_content(self):
        return self.content if len(self.content) <= 500 else f"{self.content[:500]}....."
