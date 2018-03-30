from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    #/account/username
    url(r'^(?P<username>\w+)/$', views.profile, name='profile'),

]
