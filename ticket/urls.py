"""Ticket urls."""
from django.conf.urls import patterns, include, url

from ticket.views import comment, ticket

com_pat = \
    patterns('',
             url(r'^(?P<pk>\d+)/update$', comment.Update.as_view(), name='update'),
             url(r'^(?P<pk>\d+)/$', comment.Detail.as_view(), name='detail'),
             )

unl_pat = \
    patterns('',
             url(r'^server/(?P<server>\d+)/$', ticket.Unlink.as_view(), name='server'),
             url(r'^ticket/(?P<ticket>\d+)/$', ticket.Unlink.as_view(), name='ticket'),
             url(r'^application/(?P<application>\d+)/$', ticket.Unlink.as_view(), name='application'),
             )

urlpatterns = \
    patterns('',
             url(r'^$', ticket.Index.as_view(), name='index'),
             url(r'^create/$', ticket.Create.as_view(), name='create'),
             url(r'^(?P<pk>\d+)/$', ticket.Detail.as_view(), name='detail'),
             url(r'^(?P<pk>\d+)/update/$', ticket.Update.as_view(), name='update'),
             url(r'^(?P<pk>\d+)/unlink/', include(unl_pat, namespace='unlink')),
             # Add comment to ticket
             url(r'^(?P<pk>\d+)/reply', comment.Create.as_view(), name='reply'),
             # Assign ticket to $me.
             url(r'^(?P<pk>\d+)/seize', ticket.Seize.as_view(), name='seize'),
             # view or update existing comment, pk is now pk of the comment itself.
             url(r'^comment/', include(com_pat, namespace='comment')),
             # /tickets/filter/'needle'/  where needle == 'environment|company[slug]'
             # url(r'^filter/(?P<needle>[\w-]+)/$',     'ticket.views.Filter', name='filter'),
             )
