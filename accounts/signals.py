from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from accounts.models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def update_rank(sender, instance, created, **kwargs):
    if not created:
        rank = Profile.get_rank_from_rating(instance.rating)
        Profile.objects.filter(id=instance.id).update(rank=rank)
