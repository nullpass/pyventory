# inventory/machine/urls.py

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from . import views



ser_pat = patterns('',
                   # /inventory/servers/filter/'needle'/  where needle == 'environment|company[slug]'
                   url(r'^filter/(?P<needle>[\w-]+)/$',     'inventory.views.ServerFilterView', name='filter'),
                   #
                   url(r'^(?P<pk>\d+)/$',        views.Detail.as_view(), name='detail'),
                   url(r'^(?P<pk>\d+)/update$',  views.Update.as_view(), name='update'),
                   url(r'^create/$',             views.Create.as_view(), name='create'),
                   url(r'^$',                    views.List.as_view(),   name='list'),
                   )


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name='inventory/machine/index.html'), name='index'),
    #
    url(r'^server/', include(ser_pat, namespace='server')),
)



"""



urlpatterns = patterns('',
    url(r'^$', views.InventoryIndex.as_view(), name='list'), # inventory:<list>
    #
    url(r'^domains/',      include(domains_patterns,     namespace='domains')),      # inventory:<domains>:list
    url(r'^servers/',      include(servers_patterns,     namespace='servers')),      # inventory:<servers>:list
    url(r'^environments/', include(environment_patterns, namespace='environments')), # inventory:<environments>:list
)
"""
