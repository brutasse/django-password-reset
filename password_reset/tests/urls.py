from django.conf.urls import url

from ..urls import urlpatterns
from . import views

urlpatterns += [
    url(r'^email_recover/$', views.email_recover, name='email_recover'),
    url(r'^username_recover/$', views.username_recover,
        name='username_recover'),
    url(r'^insensitive_recover/$', views.insensitive_recover,
        name='insensitive_recover'),
]
