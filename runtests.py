#!/usr/bin/env python
import os
import sys
import warnings

import django
from django.test.runner import DiscoverRunner

warnings.simplefilter('always')

os.environ['DJANGO_SETTINGS_MODULE'] = 'password_reset.tests.settings'


def runtests():
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    django.setup()

    runner = DiscoverRunner(verbosity=1, interactive=True,
                            failfast=bool(os.environ.get('FAILFAST')))
    failures = runner.run_tests(())
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
