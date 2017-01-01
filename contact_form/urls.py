from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    url(r'^$', views.contact, name='contact'),
]
