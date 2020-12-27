from django.db.models.signals import post_save
from django.dispatch import receiver

from problemset.judge import compile_submission
from problemset.models import Submission


@receiver(post_save, sender=Submission)
def compile_solution(sender, instance, created, **kwargs):
    if created:
        compile_submission(instance)


@receiver(post_save, sender=Submission)
def update_standings(sender, instance, created, **kwargs):
    contest = instance.contest
    if not created and contest and instance.status != 'Running' and contest.state == 'Running':
        problem_ids = contest.problem_ids
        problem_scores = contest.problem_scores
        standings = contest.standings
        user = instance.user

        try:
            """
            Getting index of the submitted problem and score depending on submission state
            """
            index = problem_ids.index(instance.problem_id)
            score = problem_scores[index] if instance.status == 'AC' else 0

            """
            Getting current_data for the user if available
            Otherwise generating a new dictionary containing initial values
            """
            current_data = [standing for standing in standings if standing.get('id') == user.id]
            if not current_data:
                current_data = {
                    'id': user.id,
                    'username': user.username,
                    'rank': user.profile.rank,
                    'total_score': 0,
                    'scores_per_problem': [0 for _ in problem_scores]
                }
            else:
                standings = [standing for standing in standings if standing.get('id') != user.id]
                current_data = current_data[0]

            """
            Updating user scores and calculating total scores attained
            """
            current_data.get('scores_per_problem', [])[index] = score
            total_score = 0
            for attained_score in current_data.get('scores_per_problem', []):
                total_score += attained_score
            current_data['total_score'] = total_score

            """
            Updating standings and sorting based on total score
            """
            standings.append(current_data)
            standings = sorted(standings, key=lambda x: -x['total_score'])
            contest.standings = standings
            print(standings)
            contest.save(update_fields=['standings', 'modified_at'])

        except IndexError:
            print("Index Error")
            pass



