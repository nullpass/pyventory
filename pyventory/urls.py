from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from cfgpyventory import LOCAL_ADMIN_URL

from .views import Install


urlpatterns = patterns('',
                       url(r'^inventory/', include('inventory.urls', namespace='inventory')),
                       #
                       url(r'^install/', Install.as_view(), name='shazzam'),
                       #
                       url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
                       #
                       url(LOCAL_ADMIN_URL, include(admin.site.urls)),
                       )
