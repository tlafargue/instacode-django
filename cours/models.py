from django.db import models

class Cours(models.Model):
    topic = models.CharField(max_length=100)
    video = models.CharField(max_length=500)
    text = models.TextField(max_length=10000)
    url = models.CharField(max_length=100)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.topic


class Exercice(models.Model):
    Exo = models.ForeignKey(Cours, on_delete=models.CASCADE)
    Nom_Exo = models.CharField(max_length=100)
    Choix_multiple = models.BooleanField(default=False)
    Enonce = models.TextField(max_length=10000)
    Reponse = models.CharField(max_length=10000)
    def __str__(self):
        return self.Nom_Exo
