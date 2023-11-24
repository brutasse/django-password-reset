from django.urls import path

from ..urls import urlpatterns
from . import views

urlpatterns += [
    path('email_recover/', views.email_recover, name='email_recover'),
    path('username_recover/', views.username_recover,
         name='username_recover'),
    path('insensitive_recover/', views.insensitive_recover,
         name='insensitive_recover'),
]
