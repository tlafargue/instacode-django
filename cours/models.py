from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from tinymce.models import HTMLField

class Cours(models.Model):
    titre = models.CharField(max_length=100)
    description = HTMLField()

    date_pub = models.DateTimeField('date publié')

    class Meta:
        verbose_name_plural = "cours"

    def __str__(self):
        return self.titre

    @property
    def is_pub(self):
        return self.date_pub <= timezone.now()


class Chapitre(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    video_id = models.CharField(max_length=11)
    intro = HTMLField()

    slug = models.SlugField(unique=True, blank=True)
    date_pub = models.DateTimeField('date publié')

    def __str__(self):
        return self.titre

    @property
    def is_pub(self):
        return self.date_pub <= timezone.now()

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(**kwargs)


class Exercice(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100)
    probleme = HTMLField()
    reponse = models.TextField()

    def __str__(self):
        return self.titre


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True)
    solved_exercices = models.ManyToManyField(Exercice)
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)
    interest = models.CharField(max_length=30)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
