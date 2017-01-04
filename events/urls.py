from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    url(r'^events/', views.events_list, name='events_list'),
    url(r'^event/(?P<pk>[0-9]+)/$', views.event_detail, name='event_detail'),
    url(r'^event_new/$', views.event_new, name='event_new'),
    url(r'^event/(?P<pk>[0-9]+)/edit/$', views.event_edit, name='event_edit'),
    url(r'^event/(?P<pk>\d+)/remove/$', views.event_remove, name='event_remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
