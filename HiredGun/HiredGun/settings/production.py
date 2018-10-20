import os

from HiredGun.settings.common import *

# To run with production instead of development settings,
# set the DJANGO_SETTINGS_MODULE environment variable to 'HiredGun.settings.production'

DEBUG = True

# Generate a secret.txt by:
# head -c 256 /dev/urandom | md5sum | cut -f 1 -d\ > secret.txt
SECRET_KEY = open(os.path.join(BASE_DIR, 'secret.txt')).read().strip()

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}
