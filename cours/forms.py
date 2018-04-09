from django import forms
from .models import Topic, Post, ProfaneWord
from .settings import *

class ExerciceForm(forms.ModelForm):
    class Meta():
        model = Topic
        fields = ['title', 'description']

