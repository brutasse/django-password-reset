Signals
=======

``password_reset.signals.user_recovers_password``
-------------------------------------------------

This signal is sent after a user successfully recovers their password. It
provides the ``user`` instance as well as the ``request`` object from the
view.
