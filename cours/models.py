from django.db import models

class Cours(models.Model):
    topic = models.CharField(max_length=100)
    video = models.CharField(max_length=500)
    text = models.CharField(max_length=5000)
    Photo = models.FileField()
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.topic


class Exercice(models.Model):
    Exo = models.ForeignKey(Cours, on_delete=models.CASCADE)
    Nom_Exo = models.CharField(max_length=100)
    Choix_multiple = models.BooleanField(default=False)
    Enonce = models.CharField(max_length=5000)
    Reponse = models.CharField(max_length=5000)
    def __str__(self):
        return self.song_title
