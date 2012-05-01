Welcome to django-password-reset's documentation!
=================================================

Class-based views for password reset, the usual "forget password?" workflow:

* User fills his email address or username
* Django sends him an email with a token to reset his password
* User chooses a new password

The token is not stored server-side, it is generated using Django's signing
functionality.

* Author: Bruno Renié and `contributors`_
* Licence: BSD
* Compatibility: Django 1.4+ (cryptographic signing needed)

.. _contributors: https://github.com/brutasse/django-password-reset/contributors

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   views


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
