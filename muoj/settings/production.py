from .staging import *

# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_production.sqlite3',
    }
}
