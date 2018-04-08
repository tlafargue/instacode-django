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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include


urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', include('cours.urls')),
    path('', include('registration.urls')),
    path('forum/', include('forum.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('avantages-python/', TemplateView.as_view(template_name='python.html'), name='avantages-python'),
    path('cest-quoi/', TemplateView.as_view(template_name='cest-quoi.html'), name='cest-quoi'),
    path('mentions-legales/', TemplateView.as_view(template_name='mentions-legales.html'), name='mentions-legales'),
    path('outils-developpement/', TemplateView.as_view(template_name='outils.html'), name='outils-developpement'),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
