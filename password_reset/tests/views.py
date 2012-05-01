from django.core.urlresolvers import reverse_lazy

from .. import views


class EmailRecover(views.Recover):
    search_fields = ['email']
    url = reverse_lazy('email_recover')
email_recover = EmailRecover.as_view()


class UsernameRecover(views.Recover):
    search_fields = ['username']
    url = reverse_lazy('username_recover')
username_recover = UsernameRecover.as_view()
