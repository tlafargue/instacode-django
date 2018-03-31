"""instacode_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path

from account import views
from account.views import login_view, logout_view, register_view
from django.views.generic import TemplateView

urlpatterns = [
    #/admin
    url(r'^admin/', admin.site.urls),
    #Nothing
    path('', views.home, name='home'),
    url(r'^account/', include('account.urls')),
    url(r'^login/', login_view ,name='login'),
    url(r'^logout/', logout_view ,name='logout'),
    url(r'^register/', register_view ,name='register'),
    url(r'^quoi/', views.cestquoi, name='quoi'),
    url(r'^outils/', views.outils, name='outils'),
    url(r'^avantage/', views.avantage, name='avantage'),
    url(r'^mentions/', views.mention, name='mentions'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^account/', include('account.urls'))
]
