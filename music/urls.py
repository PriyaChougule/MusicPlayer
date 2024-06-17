from django.contrib import admin
from django.urls import path,re_path
from . import views

urlpatterns = [
   
    re_path('^$',views.index,name="index"),
    re_path('^register/$',views.UserFormView.as_view(), name='register'),
    re_path('^login_user/$', views.login_user, name='login_user'),
    re_path('^(?P<album_id>[0-9]+)/$',views.detail, name='detail'),
    re_path('^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    re_path('^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    
]
