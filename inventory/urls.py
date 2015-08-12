"""Inventory URLs

namespaces
    inventory:(application|domain|server):(create|detail|index|update)

"""
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from inventory.views import application, server, domain, company, department

application_patterns = \
    patterns('',
             url(r'^create$',              application.Create.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        application.Detail.as_view(), name='detail'),
             url(r'^$',                    application.List.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', application.Update.as_view(), name='update'),
             )


server_patterns = \
    patterns('',
             url(r'^create$',              server.Create.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        server.Detail.as_view(), name='detail'),
             url(r'^$',                    server.List.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', server.Update.as_view(), name='update'),
             )

domain_patterns = \
    patterns('',
             url(r'^create$',              domain.Create.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        domain.Detail.as_view(), name='detail'),
             url(r'^$',                    domain.List.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', domain.Update.as_view(), name='update'),
             )

company_patterns = \
    patterns('',
             url(r'^create$',              company.Create.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        company.Detail.as_view(), name='detail'),
             url(r'^$',                    company.List.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', company.Update.as_view(), name='update'),
             )

depart_patterns = \
    patterns('',
             url(r'^create$',              department.Create.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$',        department.Detail.as_view(), name='detail'),
             url(r'^$',                    department.List.as_view(),   name='list'),
             url(r'^update/(?P<pk>\d+)/$', department.Update.as_view(), name='update'),
             )

urlpatterns = \
    patterns('',
             url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
             url(r'^application/', include(application_patterns, namespace='application')),
             url(r'^domain/', include(domain_patterns, namespace='domain')),
             url(r'^server/', include(server_patterns, namespace='server')),
             url(r'^company/', include(company_patterns, namespace='company')),
             url(r'^department/', include(depart_patterns, namespace='department')),
             )
