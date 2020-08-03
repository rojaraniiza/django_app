from django.conf.urls import url, include
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
from django.contrib.auth import views as auth 
from django.conf import settings
from django.contrib.auth.views import LogoutView
urlpatterns = [
    url(r'^$', views.Login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^students/$', views.students, name='students'),
    url(r'^billing/$', views.billing, name='billing'),
    url(r'^recoverpassword/$', views.recoverpw, name='recoverpw'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),  
    url(r'^logout/$', LogoutView.as_view(), name='logout'),   
    url(r'^profile/$', views.profile, name='profile'),     
]