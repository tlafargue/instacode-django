from django.contrib.auth.decorators import login_required
from django.urls import path


from . import views

app_name = 'cours'
urlpatterns = [
    path('<int:cours>/', login_required(views.CoursDetailView.as_view()), name='cours-detail'),
    path('<int:cours>/<slug:chapitre>/', login_required(views.ChapitreDetailView.as_view()), name='chapitre-detail'),
]
