import os, sys
from django.conf import settings
import django

try:
  from facebook_api_key import FACEBOOK_ACCESS_TOKEN, FACEBOOK_APP_ID, FACEBOOK_PAGE_ID
except:
  print ("You'l need a facebook api key to test this module. Put it in facebook_api_key.py")
  sys.exit(-1)

settings.configure(DEBUG=True,
               DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                    }
                },

               ROOT_URLCONF='myapp.urls',
               FACEBOOK_ACCESS_TOKEN=FACEBOOK_ACCESS_TOKEN,
               FACEBOOK_APP_ID=FACEBOOK_APP_ID,
               FACEBOOK_PAGE_ID=FACEBOOK_PAGE_ID,
               INSTALLED_APPS=('django.contrib.auth',
                              'django.contrib.contenttypes',
                              'django.contrib.sessions',
                              'django.contrib.admin',
                              'drops',))

from django.test.runner import DiscoverRunner
django.setup()
test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests(['drops'])
if failures:
    sys.exit(failures)
