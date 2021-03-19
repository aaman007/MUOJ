from celery.utils.log import get_task_logger

from muoj.celery import app
from problemset.judge import JudgeX
from problemset.models import Submission

logger = get_task_logger(__name__)


def _print_exception(e: Exception, prefix: str = None):
    prefix = f'{prefix} | ' if prefix else ''
    logger.error(f"{prefix}{type(e).__name__} | {e}")


@app.task(name="task_compile_solution")
def task_compile_solution(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
    except (Submission.DoesNotExist, Exception) as e:
        return _print_exception(e, f"submission_id : {submission_id}")

    judge = JudgeX(submission)
    judge.compile_and_update()

    logger.info("task_compile_solution executed")
