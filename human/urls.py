"""Human urls."""
from django.conf.urls import patterns, url

from human.views import account


urlpatterns = \
    patterns('',
             url(r'^login', account.Login.as_view(), name='login'),
             url(r'^logout', account.Logout.as_view(), name='logout'),
             url(r'^profile', account.Profile.as_view(), name='profile'),
             )
