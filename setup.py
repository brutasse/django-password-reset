# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst', 'r', encoding='utf-8') as f:
    long_description = f.read()

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
    long_description_content_type='text/x-rst',
    install_requires=[
        'Django>=4.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 5.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False,
)
