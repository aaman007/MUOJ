from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    institution = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    rating = models.IntegerField(default=0)
    rank = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)
    #
    #     img = Image.open(self.image.path)
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
