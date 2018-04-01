from django.shortcuts import render, get_object_or_404
from .models import Cours, Exercice


# Create your views here.
def dashboard(request):
    if (request.user.is_authenticated)==False:
        return redirect('login')
    person = request.user
    all_cours = Cours.objects.all()
    context = {'user': person, 'cours': all_cours}
    return render(request, 'account/Dashboard.html',context)

def topic(request,topic):
    if (request.user.is_authenticated)==False:
        return redirect('login')
    person = request.user
    cours = get_object_or_404(Cours, url=topic)
    print('hi')
    context = {'user': person, 'cours': cours}
    return render(request, 'account/cours_topic.html', context)


