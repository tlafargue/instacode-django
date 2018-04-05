from django.contrib.auth import views as auth_views
from django.urls import path, include

from . import views

appname = 'registration'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
