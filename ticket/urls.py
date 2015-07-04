from django.conf.urls import patterns, include, url

from . import views

com_pat = \
    patterns('',
             url(r'^(?P<pk>\d+)/$', views.CommentUpdate.as_view(), name='update'),
             url(r'^(?P<pk>\d+)/$', views.CommentDetail.as_view(), name='detail'),
             # url(r'^create$',       views.Create.as_view(), name='create'),
             # url(r'^$',             views.List.as_view(),   name='index'),
             )

urlpatterns = \
    patterns('',
             url(r'^$', views.Index.as_view(), name='index'),
             url(r'^create/$', views.Create.as_view(), name='create'),
             url(r'^(?P<environment>\w+)-(?P<pk>\d+)/$', views.Detail.as_view(), name='detail'),
             url(r'^(?P<environment>\w+)-(?P<pk>\d+)/update/$', views.Update.as_view(), name='update'),
             # Add comment to ticket
             url(r'^(?P<environment>\w+)-(?P<pk>\d+)/reply', views.Reply.as_view(), name='reply'),
             # view or update existing comment, pk is now pk of the comment itself.
             url(r'^comment/', include(com_pat, namespace='comment')),
             # /tickets/filter/'needle'/  where needle == 'environment|company[slug]'
             # url(r'^filter/(?P<needle>[\w-]+)/$',     'ticket.views.Filter', name='filter'),
             )
