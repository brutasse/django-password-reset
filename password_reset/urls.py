from django.urls import path

from . import views


urlpatterns = [
    path('recover/<str:signature>/', views.recover_done,
         name='password_reset_sent'),
    path('recover/', views.recover, name='password_reset_recover'),
    path('reset/done/', views.reset_done, name='password_reset_done'),
    path('reset/<str:token>/', views.reset,
         name='password_reset_reset'),
]
