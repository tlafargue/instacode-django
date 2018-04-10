from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .models import Cours, Chapitre, Exercice, Question, Choice, Answer


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
        print(query_set)
        print(answers)
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

