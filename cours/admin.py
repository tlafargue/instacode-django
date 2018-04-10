from django.contrib import admin
from .models import Cours, Chapitre, Exercice, Profile, Question, Answer, Choice

# Register your models here.

class CoursAdmin(admin.ModelAdmin):
    list_display = ["titre", "date_pub"]
    list_filter = ["date_pub"]

class ChapitreAdmin(admin.ModelAdmin):
    list_display = ["titre", "date_pub"]
    list_filter = ["date_pub"]

class AnswerAdmin(admin.ModelAdmin):
    list_filter = ["user"]


admin.site.register(Answer,AnswerAdmin)
admin.site.register(Chapitre, ChapitreAdmin)
admin.site.register(Choice)
admin.site.register(Cours, CoursAdmin)
admin.site.register(Exercice)
admin.site.register(Profile)
admin.site.register(Question)


