from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from cfgpyventory import LOCAL_ADMIN_URL

from .views import Install, Profile
from human.views import Login, Logout


urlpatterns = patterns('',
                       url(r'^recent/$', Profile.as_view(), name='recent'),
                       #
                       url(r'^accounts/login', Login.as_view(), name='login'),
                       url(r'^accounts/logout', Logout.as_view(), name='logout'),
                       url(r'^accounts/profile/$', Profile.as_view(), name='profile'),
                       #
                       url(r'^inventory/', include('inventory.urls', namespace='inventory')),
                       #
                       url(r'^ticket/', include('ticket.urls', namespace='ticket')),
                       #
                       url(r'^install/', Install.as_view(), name='shazzam'),
                       #
                       url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
                       #
                       url(LOCAL_ADMIN_URL, include(admin.site.urls)),
                       )
