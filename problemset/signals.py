from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile
from problemset.tasks import task_compile_solution
from problemset.models import Submission
from training.models import Tutorial


@receiver(post_save, sender=Submission)
def compile_solution(sender, instance, created, **kwargs):
    if created:
        task_compile_solution.apply_async(args=(instance.id,), countdown=10)


@receiver(post_save, sender=Submission)
def update_user_level(sender, instance, created, **kwargs):
    if instance.status == 'AC':
        """
        Updates user level for training based on solved problems
        """
        user = instance.user
        solved_ids = {
            submission.problem.id
            for submission in Submission.objects.filter(user=user, status='AC')
        }

        updated_level = user.profile.levels_completed
        for tutorial in Tutorial.objects.filter(level__gte=user.profile.levels_completed):
            common = solved_ids.intersection(set(tutorial.problem_ids))
            if len(common) != len(tutorial.problem_ids):
                break
            updated_level += 1

        Profile.objects.filter(id=user.id).update(levels_completed=updated_level)
