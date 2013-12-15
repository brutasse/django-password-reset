Signals
=======

user_recovers_password
----------------------

This signal is sent after users recover their passwords. Of course you could do extra
processing on the user by subclassing the view::

    class Register(views.Register):
        def form_valid(self, form):
            response = super(Register, self).form_valid(form)
            # do extra processing here
            return response
            
But then you can't use ``password_reset.urls`` directly since you need to swap a view.
A signal is provided for this reason.
