Customization
=============

The preferred way to customize django-password-reset is by subclassing its
views.  Configuration via Django's settings is not supported.  (After all, is
the ``case_sensitive`` or ``token_expires`` parameter really going to change
between local development, staging, and production?)

Although subclassing is preferred, django-password-view settings are
implemented as class attributes, so they can be overridden by setting views'
class attributes in your application's startup code.  For example, you could
enable case insensitive matching by adding the following code to your root
``urls.py``.  Note that this behavior may change without warning in a future
version of django-password-reset.

::

    import password_reset.views
    password_reset.views.Recover.case_sensitive = False

