try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    # get_user_model = lambda: User  # noqa

    def my_user():      # to satisfy lint in Travis auto build on Github
        return User     # noqa

    get_user_model = my_user


def get_username(user):
    username_field = getattr(user, 'USERNAME_FIELD', 'username')
    return getattr(user, username_field)
