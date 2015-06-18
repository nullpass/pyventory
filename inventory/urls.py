# inventory/urls.py

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from . import views

domain_patterns = patterns('',
    url(r'^create$',       views.DomainCreate.as_view(), name='create'),
    url(r'^$',             views.DomainList.as_view(),   name='list'),
    url(r'^(?P<pk>\d+)/$', views.DomainUpdate.as_view(), name='update'),
)

environment_patterns = patterns('',
    #url(r'^(?P<pk>\d+)/$',        views.EnvironmentDetail.as_view(), name='detail'),
    #url(r'^(?P<pk>\d+)/update$',  views.EnvironmentUpdate.as_view(), name='update'),
    #url(r'^create/$',             views.EnvironmentCreate.as_view(), name='create'),
    url(r'^$',                    views.EnvironmentList.as_view(),   name='list'),
)


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='inventory/home.html')),
    #
    url(r'^domain/',      include(domain_patterns,      namespace='domain')),      # inventory:<domain>:list
    url(r'^environment/', include(environment_patterns, namespace='environment')), # inventory:<environment>:list
)



"""

servers_patterns = patterns('',
    # /inventory/servers/filter/'needle'/  where needle == 'environment|company[slug]'
    url(r'^filter/(?P<needle>[\w-]+)/$',     'inventory.views.ServerFilterView', name='filter'),
    #
    url(r'^(?P<pk>\d+)/$',        views.ServerDetail.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update$',  views.ServerUpdate.as_view(), name='update'),
    url(r'^create/$',             views.ServerCreate.as_view(), name='create'),
    url(r'^$',                    views.ServerList.as_view(),   name='list'),
)


urlpatterns = patterns('',
    url(r'^$', views.InventoryIndex.as_view(), name='list'), # inventory:<list>
    #
    url(r'^domains/',      include(domains_patterns,     namespace='domains')),      # inventory:<domains>:list
    url(r'^servers/',      include(servers_patterns,     namespace='servers')),      # inventory:<servers>:list
    url(r'^environments/', include(environment_patterns, namespace='environments')), # inventory:<environments>:list
)
"""
