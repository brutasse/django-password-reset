def get_current_site():
    try:
        from django.contrib.sites.shortcuts import get_current_site
    except ImportError:
        from django.contrib.sites.models import get_current_site
    return get_current_site
