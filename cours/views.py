from django.contrib.auth.decorators import login_required
from django.views import generic
from django.utils import timezone

from .models import Cours, Chapitre, Exercice

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
