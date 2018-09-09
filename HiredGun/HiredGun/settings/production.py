import os

from HiredGun.settings.common import *

# To run with production instead of development settings,
# set the DJANGO_SETTINGS_MODULE environment variable to 'HiredGun.settings.production'

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')
