from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'cours'
urlpatterns = [
    path('classement/', login_required(views.LeaderboardView.as_view()), name='leaderboard'),
    path('cours/<int:cours>/', login_required(views.CoursDetailView.as_view()), name='cours-detail'),
    url(r'^cours/(?P<cours_id>[0-9]+)/(?P<chapitre_id>[0-9]+)/', login_required(views.ChapitreDetailView.as_view()), name='chapitre-detail'),
    path('profile/<str:username>/', login_required(views.ProfileDetailView.as_view()), name='profile-detail'),
    url(r'^reset/(?P<chap_id>[0-9]+)/', login_required(views.reset),name='reset'),

]
