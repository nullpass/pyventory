"""Human urls."""
from django.conf.urls import patterns, url

from human.views import account, department


urlpatterns = \
    patterns('',
             url(r'^login', account.Login.as_view(), name='login'),
             url(r'^logout', account.Logout.as_view(), name='logout'),
             url(r'^profile', account.Profile.as_view(), name='profile'),
             url(r'^foo', department.Create.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$', department.Detail.as_view(), name='detail'),
             url(r'^update/(?P<pk>\d+)/$', department.Update.as_view(), name='update'),
             url(r'^departments/$', department.List.as_view(), name='list'),
             )
