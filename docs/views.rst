Views
=====

.. note::

    The ``Recover`` and ``Reset`` views share a common attribute, ``salt``.
    This is the `salt used for signing the password reset link`_, it is useful
    for avoiding collisions with values you may have signed elsewhere in your
    app. It doesn't need to be complicated, just distinct from other salts
    you're using in your code. More importantly, the salt must be the same on
    the ``Recover`` and the ``Reset`` views. The default salt is
    ``password_recovery``. If you're not already using this as a salt
    somewhere else in your app, you don't need to alter it.

    Additionally, there is a ``url_salt`` used for redirecting the user after
    he has entered his username or email. This salt **must** be different than
    the other one. Its default value is ``password_recovery_url``.

    .. _salt used for signing the password reset link: https://docs.djangoproject.com/en/dev/topics/signing/#using-the-salt-argument

Recover
-------

This is a ``FormView`` that asks for a username or email, finds the
corresponding user object and sends him an email.

Attributes
``````````

* ``case_sensitive``: whether to search case-sensitively based on the form
  data. Default: ``True``.

* ``form_class``: the form to use for validating the user. Default:
  ``password_reset.forms.PasswordRecoveryForm``. To customize form error
  messages, subclass the form and override the ``error_messages`` attribute.

* ``success_url_name``: the name of the URL to redirect to after sending the
  recovery email. Change it if you don't use the provided URLconf. Defaults to
  ``password_reset_sent``.

* ``template_name``: defaults to ``password_reset/recovery_form.html``.

* ``email_template_name``: the template to use for sending the reset link by
  email. Default: ``password_reset/recovery_email.txt``.

* ``email_subject_template_name``: the template to use for generating the
  email subject. Defaults to ``password_reset/recovery_email_subject.txt``.

* ``search_fields``: the fields to search for on the ``User`` model. Default
  is ``['username', 'email']``, you can restrict it to ``['username']`` or
  ``['email']`` but no other fields are supported, at least not with the
  default form class.

Methods
```````

* ``send_notification()``: this builds the email context, loads the template
  and sends the password reset email.

* ``get_site()``: method to obtain the website's host name.  This method first 
  checks and sets the site from the optional `Django sites framework
  <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_.  If missing,
  it will deduce the domain and name by looking at the request object's domain.

RecoverDone
-----------

This is a ``TemplateView`` to confirm the user that an email was sent.

Attributes
``````````

* ``template_name``: ``password_reset/reset_sent.html``

Template Context
````````````````

``invalid`` Set to ``True`` if the URL signature isn't valid, which happens if
you change your ``SECRET_KEY``, the ``url_salt`` or if people try to
reverse-engineer your URLs.

``email``: the username or email of the user.

``timestamp``: the time the signature was issues, which normally corresponds
to the time the reset email was sent.

Reset
-----

Attributes
``````````

* ``form_class``: defaults to ``password_reset.forms.PasswordResetForm``. To
  customize form error messages, subclass the form and override the
  ``error_messages`` attribute.

* ``token_expires``: expiration time (in seconds) of the password reset token.
  Default is two days.

* ``template_name``: defaults to ``password_reset/reset.html``.

* ``success_url``: the URL to redirect to after a successful password reset.
  Defaults to ``reverse_lazy('password_reset_done')``, change it if you don't
  use the provided URLconf.

Methods
```````

* ``invalid()``: this method builds the response returned when an invalid
  token is encountered.

ResetDone
---------

This is a simple ``TemplateView`` that displays a success message. Its default
``template_name`` is ``password_reset/recovery_done.html``.
