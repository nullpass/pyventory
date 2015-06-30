from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^(?P<pk>\d+)/$', views.Update.as_view(), name='update'),
                       url(r'^create$',       views.Create.as_view(), name='create'),
                       url(r'^$',             views.List.as_view(),   name='index'),
                       )