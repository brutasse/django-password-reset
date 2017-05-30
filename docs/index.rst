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
   signals

Changelog
---------

* 1.0 (2017-05-30):

  * Drop support for Django < 1.8 and confirm support for Django 1.10 and 1.11.

* 0.9 (2016-06-01):

  * Allow token expiration time to be customized with a setting.

* 0.8.2 (2016-01-12):

  * Django 1.9 compatibility (Josh Kelley).

* 0.8.1 (2015-10-30):

  * Add pt_BR translation (GitHub user eduardo-matos).

* 0.8 (2015-10-30):

  * Allow customizing form error message via the ``error_messages`` attribute
    on form classes.

  * Add Georgian translation (GitHub user gigovich).

  * Add Norwegian translation (GitHub user gunnaringe).

  * Tested on django 1.5 to 1.8 and Python 2.6 to 3.4.

* 0.7 (2014-02-18):

  * Return user instance in ``PasswordResetForm.save()``, add ``commit``
    keyword argument.

* 0.6.1 (2014-02-14):

  * Fix for custom user models without any field named ``username``.
    Properly take ``USERNAME_FIELD`` into account.

  * Add German translation (GitHub user billyBlaze).

  * Add Chinese translation (GitHub user saggit).

* 0.6 (2013-12-15):

  * New ``user_recovers_password`` signal (José Sazo).

* 0.5.1 (2013-10-31):

  * Spanish, Polish and Russian translations.

* 0.5 (2013-05-19):

  * Support for Django 1.5's custom user model.

* 0.4 (2013-02-18):

  * Python3 and Django 1.5 support.

* 0.3:

  * The recover view now redirects to a signed URL to avoid duplicate
    submissions.
  * Bugfix: made ``case_sensitive`` work properly when set to ``False``.

* 0.2: Bugfix: actually save the new password.
* 0.1: Initial version.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
