from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .forms import UpdateProfile
from .models import Cours, Chapitre, Answer, Profile
from django.core.files.storage import FileSystemStorage



class ChapitreDetailView(TemplateView):
    template_name = 'cours/chapitre-detail.html'
    def get(self, request, cours_id, chapitre_id):
        chap = get_object_or_404(Chapitre,pk=chapitre_id)
        user = request.user
        answers = Answer.objects.filter(user=user.id).order_by('id')
        context = {'chapitre':chap, 'answers': answers}
        return render(request, self.template_name, context)
    def post(self, request , cours_id, chapitre_id):
        chap = get_object_or_404(Chapitre,pk=chapitre_id)
        user = request.user
        query_set = []
        answers=[]
        for exo in chap.exercice_set.all():
            for question in exo.question_set.all():
                for choice in question.choice_set.all():
                    if question.is_multiplechoice:
                        query_set.append(request.POST.get(str(choice.id), False))
                        answers.append(get_object_or_404(Answer,user=user.id, choice=choice.id))
                    else:
                        query_set.append(request.POST.get(str(question.id), False))
                        answers.append(get_object_or_404(Answer,user=user.id, choice=choice.id))
        for i in range(len(answers)):
            a=int(answers[i].choice.id)
            b=int(query_set[i])
            if (a==b):
                Answer.objects.filter(pk=answers[i].id).update(answer=True)
            Answer.objects.filter(pk=answers[i].id).update(show_answer=True)

        answers = Answer.objects.filter(user=user.id).order_by('id')
        context = {'chapitre': chap, 'answer': answers}
        return render(request, self.template_name, context)


class CoursDetailView(generic.DetailView):
    model = Cours
    template_name = 'cours/cours-detail.html'
    pk_url_kwarg = 'cours'

    def get_queryset(self):
        return Cours.objects.filter(date_pub__lte=timezone.now())


class ProfileDetailView(generic.DetailView):
    model = User
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs['username'])










class CompteDetailView(TemplateView):
    template_name = 'compte.html'
    def get(self, request):
        form = UpdateProfile()
        user = request.user
        context = {'user': user, 'form':form}
        return render(request, self.template_name, context)
    def post(self, request):
        user = request.user
        form = UpdateProfile(request.POST,request.FILES)
        print(form.is_valid())
        if form.is_valid():
            email = form.cleaned_data['email']
            nom_complet = form.cleaned_data['nom_complet']
            langue = form.cleaned_data['langue']
            a_propos = form.cleaned_data['a_propos']
            ville = form.cleaned_data['ville']
            pays = form.cleaned_data['pays']
            birth_date = form.cleaned_data['birth_date']
            niveau_de_formation = form.cleaned_data['niveau_de_formation']
            gender = form.cleaned_data['gender']
            image = form.cleaned_data['image']
            if (image == None):
                image = user.profile.image
            else:
                fs = FileSystemStorage()
                fs.save(image.name,image)
            User.objects.filter(id=user.id).update(email=email)
            Profile.objects.filter(user=user.id).update(nom_complet=nom_complet,langue=langue,a_propos=a_propos,ville=ville,pays=pays,birth_date=birth_date,niveau_de_formation=niveau_de_formation,gender=gender, image=image)
            return redirect("cours:profile-detail", user.username)
        context = {'user': user, 'form': form}
        return render(request, self.template_name, context)












class LeaderboardView(generic.ListView):
    template_name = 'leaderboard.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.order_by('-profile__points')


def reset(request,chap_id):
    user = request.user
    answers = []
    chap = get_object_or_404(Chapitre, pk=chap_id)
    if request.method == 'POST':
        for exo in chap.exercice_set.all():
            for question in exo.question_set.all():
                for choice in question.choice_set.all():
                    answers.append(get_object_or_404(Answer, user=user.id, choice=choice.id))

        for i in range(len(answers)):
            Answer.objects.filter(pk=answers[i].id).update(show_answer=False,answer=False)
        a=chap.cours.id
        b=chap.id
        return redirect('cours:chapitre-detail', a,b)
    return render(request,'cours/resetform.html')

