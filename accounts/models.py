from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.utils.translation import gettext_lazy as _
from PIL import Image


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    objects = UserManager()


class Profile(models.Model):
    class RankChoices(models.IntegerChoices):
        NEWBIE = -10000, _('Newbie')
        PUPIL = 1200, _('Pupil')
        SPECIALIST = 1400, _('Specialist')
        EXPERT = 1600, _('Expert')
        CANDIDATE_MASTER = 1900, _('Candidate Master')
        MASTER = 2100, _('Master')
        INTERNATIONAL_MASTER = 2300, 'International Master'
        GRANDMASTER = 2400, _('Grandmaster')

    user = models.OneToOneField(verbose_name=_('User'), to=User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(verbose_name=_('Picture'), default='default.jpg', upload_to='profile_pics')
    institution = models.CharField(verbose_name=_('Institution'), max_length=100)
    location = models.CharField(verbose_name=_('Location'), max_length=200)
    rating = models.IntegerField(verbose_name=_('Rating'), default=0)
    rank = models.IntegerField(verbose_name=_('Rank'), choices=RankChoices.choices, default=RankChoices.NEWBIE)
    """
    Rating History Format:
    [
        {
            'contest_id': 1,
            'contest_title': 'MU Contest 1',
            'rank': 27,
            'previous_rating': 1387,
            'new_rating': 1456
        }
    ]
    """
    rating_history = models.JSONField(verbose_name=_('Rating History'), default=list, blank=True)
    levels_completed = models.PositiveIntegerField(verbose_name=_("Current Level"), default=1)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['-id']

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

    @property
    def contest_count(self):
        return len(self.rating_history)

    @property
    def rank_label(self):
        for choice in Profile.RankChoices.choices:
            if choice[0] == self.rank:
                return choice[1]

    @staticmethod
    def get_rank_from_rating(rating):
        rank = -10000
        for choice in Profile.RankChoices.choices:
            if choice[0] <= rating:
                rank = choice[0]
        return rank
