from django.conf import settings

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

__version__ = '0.8.1'

DEFAULT_SETTINGS = {
		'token_expires': 3600 * 48,  # Two days
		'get_current_site': get_current_site
}

try:
		PASSWORD_RESET_SETTINGS = getattr(settings,
																			'PASSWORD_RESET_SETTINGS',
																			DEFAULT_SETTINGS)
except:
		PASSWORD_RESET_SETTINGS = {}

DEFAULT_SETTINGS.update(PASSWORD_RESET_SETTINGS)
print PASSWORD_RESET_SETTINGS
