Quickstart
==========

Installation
------------

Simple:

* ``pip install django-password-reset``

Usage
-----

Simple:

* Add ``password_reset`` to your ``INSTALLED_APPS``

* ``include('password_reset.urls')`` in your root ``urls.py``

* Link to the password reset page: ``{% url "password_reset_recover" %}``

* Create a ``password_reset/base.html`` template and adapt it to your site's
  structure

What you get
------------

* A `password reset` workflow with no data stored on the server, tokens are
  signed and checked with your ``SECRET_KEY``.

* The ability to look for your user's username or email address.

* Password reset links that expire in two days (configurable).

What you can do
---------------

* Use custom templates for everything: the email subject and body, the forms
  and confirmation pages.

* Use custom forms if you need something else than searching for username
  `or` email, or search case-insensitively.

* Use a custom salt or expiration time for tokens (expiration via
  ``PASSWORD_RESET_TOKEN_EXPIRES`` setting).

* Allow password recovery for all users (default) or only for active users (via ``RECOVER_ONLY_ACTIVE_USERS=False`` setting)

See the next section.
