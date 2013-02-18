from django.conf.urls import url, patterns

from . import views


urlpatterns = patterns(
    '',
    url(r'^recover/(?P<signature>.+)/$', views.recover_done,
        name='password_reset_sent'),
    url(r'^recover/$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
)
