from celery.utils.log import get_task_logger

from django.contrib.auth import get_user_model

from accounts.models import Profile
from contest.models import Contest
from contest.rating_system import RatingSystem
from muoj.celery import app

User = get_user_model()
logger = get_task_logger(__name__)


def _print_exception(e: Exception, prefix: str = None):
    prefix = f'{prefix} | ' if prefix else ''
    logger.error(f"{prefix}{type(e).__name__} | {e}")


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    pass


@app.task(name='task_apply_contest_rating')
def task_apply_contest_rating(contest_id):
    try:
        contest = Contest.objects.get(id=contest_id)
    except Exception as e:
        Contest.objects.filter(id=contest_id).update(rating_applied=False)
        return _print_exception(e, prefix=f"contest_id: {contest_id}")

    rating_system = RatingSystem(contest_id)
    rating_changes = rating_system.get_rating_changes()
    user_ranks, problems_solved = dict(), dict()

    for standing in contest.standings:
        user_ranks[standing.get('id')] = standing.get('rank')
        problems_solved[standing.get('id')] = len(standing.get('scores_per_problem'))

    user_ids = list(rating_changes.keys())

    for user_id in user_ids:
        profile = Profile.objects.get(user_id=user_id)
        current_rating = profile.rating
        rating_history = profile.rating_history
        rating_history.append({
            'contest_id': contest_id,
            'contest_title': contest.title,
            'rank': user_ranks[user_id],
            'problems_solved': problems_solved[user_id],
            'previous_rating': current_rating,
            'new_rating': current_rating + rating_changes[user_id]
        })

        profile.rating += rating_changes[user_id]
        profile.rating_history = rating_history
        profile.save(update_fields=['rating', 'rating_history'])

    logger.info('Executed task_apply_contest_rating')


