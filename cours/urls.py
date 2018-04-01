from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from . import views

app_name = 'cours'


urlpatterns = [
    #/cours/topic
    url(r'^(?P<topic>\w+)/$', views.topic, name='topic'),

]
