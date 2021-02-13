import logging
from datetime import datetime

from django.utils import timezone

from muoj import settings


def datetime_to_str(dt: datetime):
    dt = timezone.localtime(dt)
    rest_framework_setting = getattr(settings, 'REST_FRAMEWORK', {})
    assert rest_framework_setting and 'DATETIME_FORMAT' in rest_framework_setting, (
        'Add DRF config DATETIME_FORMAT in settings.py'
    )

    return dt.strftime(rest_framework_setting['DATETIME_FORMAT'])


# Logging Related Utilities
def get_logger(name='django'):
    return logging.getLogger(name)


def get_request_str(request):
    meta = request.META
    return f"{request.method} {request.get_full_path()} {meta.get('SERVER_PROTOCOL')} {meta.get('HTTP_USER_AGENT')}"


def get_debug_str(request, user, errors):
    return (
        f"""
        request: {get_request_str(request)}
        user: {f"{user} ({user.id})" if user else ""}
        data: {request.data}
        errors: {errors}"""
    )
