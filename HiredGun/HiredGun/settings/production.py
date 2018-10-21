import os

from HiredGun.settings.common import *

# To run with production instead of development settings,
# set the DJANGO_SETTINGS_MODULE environment variable to 'HiredGun.settings.production'

DEBUG = False

# Generate a secret.txt by:
# head -c 50 /dev/urandom | base64 > secret.txt
SECRET_KEY = open(os.path.join(BASE_DIR, 'secret.txt')).read().strip()

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# These were suggested by 'python3 manage.py check --deploy'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
