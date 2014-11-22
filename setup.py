# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages


setup(
    name='django-password-reset',
    version=__import__('password_reset').__version__,
    author='Bruno Renie',
    author_email='bruno@renie.fr',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/brutasse/django-password-reset',
    license='BSD licence, see LICENSE file',
    description='Class-based views for password reset.',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django>=1.4',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    test_suite='runtests.runtests',
    zip_safe=False,
)
