from django.conf.urls import url, include

from ..urls import urlpatterns
from . import views

try:
    import captcha as captcha_installed
except:
    captcha_installed = None

urlpatterns += [
    url(r'^email_recover/$', views.email_recover, name='email_recover'),
    url(r'^username_recover/$', views.username_recover,
        name='username_recover'),
    url(r'^insensitive_recover/$', views.insensitive_recover,
        name='insensitive_recover'),
]

if captcha_installed:
    urlpatterns += [
        url(r'^captcha/', include('captcha.urls')),
    ]
