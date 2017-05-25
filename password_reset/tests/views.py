from .. import views


class EmailRecover(views.Recover):
    search_fields = ['email']


email_recover = EmailRecover.as_view()


class UsernameRecover(views.Recover):
    search_fields = ['username']


username_recover = UsernameRecover.as_view()


class InsensitiveRecover(views.Recover):
    case_sensitive = False


insensitive_recover = InsensitiveRecover.as_view()
