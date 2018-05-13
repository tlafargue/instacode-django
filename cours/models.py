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

    def __str__(self):
        return self.titre

FORMATION = (('Doctorat', 'Doctorat'),
              ('Master', 'Master'),
             ('Diplome de 1er cycle', 'Diplome de 1er cycle'),
             ('Lycée', 'Lycée'),
             ('Collège', 'Collège'),
             ('Enseignement Primaire', 'Enseignement Primaire'),
             ('Education non formelle', 'Education non formelle'),
             ('Autre Education', 'Autre Education'))


CHOICES = [(i,i) for i in range(1900,2019)]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_complet = models.CharField(max_length=30, blank=True)
    langue = models.CharField(max_length=30, blank=True)
    a_propos = models.TextField(max_length=10000, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True)
    year_date = models.CharField(max_length=60,choices=CHOICES, blank=True, null=True)
    niveau_de_formation = models.CharField(max_length=60,choices=FORMATION, blank=True, null=True)
    solved_exercices = models.ManyToManyField(Exercice)
    points = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)
    interest = models.CharField(max_length=30)
    def __str__(self):
        return self.user.username



class Question(models.Model):
     exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE)
     question = models.CharField(max_length=100)
     is_multiplechoice = models.BooleanField(default=False)
     reponse = models.TextField()
     def __str__(self):
         return "Question " + str(self.id) + " to exercice "+ str(self.exercice)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    goodanswer = models.BooleanField(default=False)
    proposition = models.CharField(max_length=100)

    def __str__(self):
        return "choice of question " + str(self.question)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
    answer = models.BooleanField(default=False)
    show_answer = models.BooleanField(default=False)
    def __str__(self):
        return str(self.user) + "'s answer to proposition " + str(self.choice)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Choice)
def create_answer(sender, instance, created, **kwargs):
    if created:
        all_user = User.objects.all()
        for user in all_user:
            Answer.objects.create(choice=instance,user=User.objects.get(pk=user.id))