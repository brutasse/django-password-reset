def get_user_model():
    """
    Returns the User model that is active in this project.
    """
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
    except ImportError:
        from django.contrib.auth.models import User
    return User


def get_username(user):
    """
    Returns the name of the username field
    :param user: User object instance
    :return: str
    """
    username_field = getattr(user, 'USERNAME_FIELD', 'username')
    return getattr(user, username_field)


def get_current_site(*args, **kwargs):
    """
    Checks if contrib.sites is installed and returns either the current
    ``Site`` object or a ``RequestSite`` object based on the request.
    """
    try:
        from django.contrib.sites.shortcuts import get_current_site as current_site
    except ImportError:
        from django.contrib.sites.models import get_current_site as current_site
    return current_site(*args, **kwargs)
