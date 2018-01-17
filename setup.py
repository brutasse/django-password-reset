# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages


try:
    long_description = open('README.rst', encoding='utf-8').read()
except TypeError:
    long_description = open('README.rst').read()

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
    long_description=long_description,
    install_requires=[
        'Django>=1.8',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    test_suite='runtests.runtests',
    zip_safe=False,
)
