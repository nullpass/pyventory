# inventory/urls.py

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='inventory/index.html'), name='index'),
                       url(r'^application/', include('inventory.application.urls', namespace='application')),
                       url(r'^category/', include('inventory.category.urls', namespace='category')),
                       url(r'^domain/', include('inventory.domain.urls', namespace='domain')),
                       url(r'^environment/', include('inventory.environment.urls', namespace='environment')),
                       url(r'^machine/', include('inventory.machine.urls', namespace='machine')),
                       )
