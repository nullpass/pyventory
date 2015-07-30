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
             url(r'^$',                    views.ApplicationList.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', views.ApplicationUpdate.as_view(), name='update'),
             )

server_patterns = \
    patterns('',
             url(r'^create$',              views.ServerCreate.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        views.ServerDetail.as_view(), name='detail'),
             url(r'^$',                    views.ServerList.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', views.ServerUpdate.as_view(), name='update'),
             )

domain_patterns = \
    patterns('',
             url(r'^create$',              views.DomainCreate.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        views.DomainDetail.as_view(), name='detail'),
             url(r'^$',                    views.DomainList.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', views.DomainUpdate.as_view(), name='update'),
             )

company_patterns = \
    patterns('',
             url(r'^create$',              views.CompanyCreate.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        views.CompanyDetail.as_view(), name='detail'),
             url(r'^$',                    views.CompanyList.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', views.CompanyUpdate.as_view(), name='update'),
             )

urlpatterns = \
    patterns('',
             url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
             url(r'^application/', include(application_patterns, namespace='application')),
             url(r'^domain/', include(domain_patterns, namespace='domain')),
             url(r'^server/', include(server_patterns, namespace='server')),
             url(r'^company/', include(company_patterns, namespace='company')),
             )
