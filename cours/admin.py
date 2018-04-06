from django.contrib import admin

from .models import Cours, Chapitre, Exercice, Profile

# Register your models here.

admin.site.register(Cours)
admin.site.register(Chapitre)
admin.site.register(Exercice)
admin.site.register(Profile)
