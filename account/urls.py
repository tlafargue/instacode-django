from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
from account import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('',views.home,name='home')
]
