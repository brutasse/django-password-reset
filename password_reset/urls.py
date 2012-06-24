from django.conf.urls.defaults import url, patterns

from . import views


urlpatterns = patterns('',
    url(r'^sent/$', views.mail_sent, name='password_reset_sent'),
    url(r'^recover/$', views.recover, name='password_reset_recover'),
    url(r'^reset/done/$', views.reset_done, name='password_reset_done'),
    url(r'^reset/(?P<token>[\w:-]+)/$', views.reset,
        name='password_reset_reset'),
)
