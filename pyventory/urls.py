from django.conf.urls import patterns, include, url
from django.contrib import admin

from cfgpyventory import LOCAL_ADMIN_URL

urlpatterns = patterns('',
    url(LOCAL_ADMIN_URL, include(admin.site.urls)),
)
