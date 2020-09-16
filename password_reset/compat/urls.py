# coding=utf-8

try:
    from django.urls import reverse, reverse_lazy, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, reverse_lazy, NoReverseMatch