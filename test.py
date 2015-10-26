import os, sys
from django.conf import settings
import django

settings.configure(DEBUG=True,
               DATABASES={
                    'default': {
                        'ENGINE': 'django.db.backends.sqlite3',
                    }
                },
               ROOT_URLCONF='myapp.urls',
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
