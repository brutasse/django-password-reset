#!/usr/bin/env python
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'password_reset.tests.settings'

from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner
from django.utils.functional import empty


def runtests(*test_args):
    test_args = test_args or ['tests']
    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    runner = DjangoTestSuiteRunner(verbosity=1, interactive=True,
                                   failfast='--failfast' in sys.argv)
    failures = runner.run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
