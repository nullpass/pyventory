# inventory/urls.py

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

"""
dom_pat = patterns('',
                   url(r'^(?P<pk>\d+)/$', views.DomainUpdate.as_view(), name='update'),
                   url(r'^create$',       views.DomainCreate.as_view(), name='create'),
                   url(r'^$',             views.DomainList.as_view(),   name='index'),
                   )

env_pat = patterns('',
                   url(r'^(?P<pk>\d+)/$', views.EnvironmentUpdate.as_view(), name='update'),
                   url(r'^create/$',      views.EnvironmentCreate.as_view(), name='create'),
                   url(r'^$',             views.EnvironmentList.as_view(),   name='index'),
                   )

                       #
                       # inventory:<domain>:index
                       url(r'^domain/',      include(dom_pat, namespace='domain')),
                       #
                       # inventory:<environment>:index
                       url(r'^environment/', include(env_pat, namespace='environment')),


"""

urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
                       # url(r'^application/', include('inventory.application.urls', namespace='application')),
                       url(r'^category/', include('inventory.category.urls', namespace='category')),
                       # url(r'^domain/', include('inventory.domain.urls', namespace='domain')),
                       # url(r'^environment/', include('inventory.environment.urls', namespace='environment')),
                       url(r'^machine/', include('inventory.machine.urls', namespace='machine')),
                       )
