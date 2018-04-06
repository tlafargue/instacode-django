from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import Cours, Chapitre

# Create your views here.


class CoursDetailView(generic.DetailView):
    model = Cours
    template_name = 'cours/cours-detail.html'
    pk_url_kwarg = 'cours'

    def get_queryset(self):
        return Cours.objects.filter(date_pub__lte=timezone.now())


class ChapitreDetailView(generic.DetailView):
    model = Chapitre
    template_name = 'cours/chapitre-detail.html'
    slug_url_kwarg = 'chapitre'

    def get_queryset(self):
        return Chapitre.objects.filter(cours=self.kwargs['cours']).filter(date_pub__lte=timezone.now())


class ProfileDetailView(generic.DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])


class LeaderboardView(generic.ListView):
    template_name = 'leaderboard.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.order_by('-profile__points')
