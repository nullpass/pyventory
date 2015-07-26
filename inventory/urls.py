"""

namespaces
    inventory:(application|domain|server):(create|detail|index|update)


"""
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from . import views


application_patterns = \
    patterns('',
             url(r'^create$',              views.ApplicationCreate.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        views.ApplicationDetail.as_view(), name='detail'),
             url(r'^$',                    views.ApplicationIndex.as_view(),  name='index'),
             url(r'^update/(?P<pk>\d+)/$', views.ApplicationUpdate.as_view(), name='update'),
             )
"""
domain_patterns = \
    patterns('',
             url(r'^create$',              views.DomainCreate.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        views.DomainDetail.as_view(), name='detail'),
             url(r'^$',                    views.DomainIndex.as_view(),  name='index'),
             url(r'^update/(?P<pk>\d+)/$', views.DomainUpdate.as_view(), name='update'),
             )
"""

urlpatterns = \
    patterns('',
             url(r'^$', TemplateView.as_view(template_name='home.html'), name='index'),
             url(r'^application/', include(application_patterns, namespace='application')),
             url(r'^domain/', include('inventory.domain.urls', namespace='domain')),
             url(r'^machine/', include('inventory.machine.urls', namespace='machine')),
             )

