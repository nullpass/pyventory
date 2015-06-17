from django.conf.urls import patterns, include, url
from django.contrib import admin

from cfgpyventory import LOCAL_ADMIN_URL

from .views import Install


urlpatterns = patterns('',
                       url(r'^install/',      Install.as_view(), name='shazzam'),
                       url(LOCAL_ADMIN_URL, include(admin.site.urls)),
                       )

