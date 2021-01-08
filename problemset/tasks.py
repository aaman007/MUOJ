from celery.utils.log import get_task_logger

from muoj.celery import app

logger = get_task_logger(__name__)


def _print_exception(e: Exception, prefix: str = None):
    prefix = f'{prefix} | ' if prefix else ''
    logger.error(f"{prefix}{type(e).__name__} | {e}")


@app.task(name="task_print_hello")
def task_print_hello():
    print("HELLO")
    logger.info("task_print_hello executed")
