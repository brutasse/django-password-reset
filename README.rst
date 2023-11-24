Django-password-reset
=====================

.. image:: https://travis-ci.org/brutasse/django-password-reset.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/brutasse/django-password-reset

Class-based views for password reset, the usual "forget password?" workflow:

* User fills his email address or username
* Django sends him an email with a token to reset his password
* User chooses a new password

The token is not stored server-side, it is generated using Django's signing
functionality.

* Author: Bruno Renié and `contributors`_
* Licence: BSD
* Compatibility: Django 3+
* Python 3+
.. _contributors: https://github.com/brutasse/django-password-reset/contributors

Installation
------------

* ``pip install -U django-password-reset``
* Add ``password_reset`` to your ``INSTALLED_APPS``
* Include ``password_reset.urls`` in your root ``urls.py``

For extensive documentation see the ``docs`` folder or `read it on
readthedocs`_

.. _read it on readthedocs: https://django-password-reset.readthedocs.io/

To install the `in-development version`_ of django-password-reset, run ``pip
install django-password-reset==dev``.

.. _in-development version: https://github.com/brutasse/django-password-reset/tarball/master#egg=django-password-reset-dev

Bugs
----

Really? Oh well... Please Report. Or better, fix :)
