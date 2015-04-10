#!/usr/bin/env python
import os
import sys
import warnings

import django

warnings.simplefilter('always')

os.environ['DJANGO_SETTINGS_MODULE'] = 'password_reset.tests.settings'

try:
    from django.test.runner import DiscoverRunner
except ImportError:
    from discover_runner import DiscoverRunner


def runtests():
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    if django.VERSION >= (1, 7):
        django.setup()

    runner = DiscoverRunner(verbosity=1, interactive=True,
                            failfast=bool(os.environ.get('FAILFAST')))
    failures = runner.run_tests(())
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
