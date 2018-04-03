import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone, formats

from .models import Cours, Chapitre

# Create your tests here.


def create_cours(titre, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Cours.objects.create(titre=titre, date_pub=time)


def create_chapitre(titre, cours, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Chapitre.objects.create(titre=titre, cours=cours, date_pub=time)

def create_user(username, password):
    email = username + '@example.com'
    user = User.objects.create_user(username=username, email=email, password=password)
    return user


class CoursModelTests(TestCase):

    def test_is_pub_with_future_cours(self):
        """
        Future cours is not published
        """
        time = timezone.now() + datetime.timedelta(seconds=1)
        future_cours = Cours(date_pub=time)
        self.assertIs(future_cours.is_pub, False)

    def test_is_pub_with_past_cours(self):
        """
        Past cours is published
        """
        time = timezone.now() - datetime.timedelta(seconds=1)
        past_cours = Cours(date_pub=time)
        self.assertIs(past_cours.is_pub, True)


class ChapitreModelTests(TestCase):

    def test_is_pub_with_future_chapitre(self):
        """
        Future chapitre is not published
        """
        time = timezone.now() + datetime.timedelta(seconds=1)
        future_chapitre = Chapitre(date_pub=time)
        self.assertIs(future_chapitre.is_pub, False)

    def test_is_pub_with_past_chapitre(self):
        """
        Past chapitre is published
        """
        time = timezone.now() - datetime.timedelta(seconds=1)
        past_chapitre = Chapitre(date_pub=time)
        self.assertIs(past_chapitre.is_pub, True)


class CoursDetailViewTests(TestCase):

    def login_user(self):
        create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')

    def test_future_cours(self):
        """
        Future cours cannot be viewed
        """
        self.login_user()
        future_cours = create_cours(titre='Cours future', days=1)
        url = reverse('cours:cours-detail', args=(future_cours.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_cours(self):
        """
        Past cours can be viewed
        """
        self.login_user()
        past_cours = create_cours(titre='Cours past', days=-1)
        url = reverse('cours:cours-detail', args=(past_cours.id,))
        response = self.client.get(url)
        self.assertContains(response, past_cours.titre)

    def test_future_chapitre_in_cours(self):
        """
        Future chapitre in cours shows the date at which it will be published
        """
        self.login_user()
        cours = create_cours(titre='Cours', days=-1)
        future_chapitre = create_chapitre(titre='Chapitre future', cours=cours, days=1)
        date = formats.date_format(future_chapitre.date_pub, "j F Y")
        chapitre_url = reverse('cours:chapitre-detail', args=(cours.id, future_chapitre.slug,))
        cours_url = reverse('cours:cours-detail', args=(cours.id,))
        response = self.client.get(cours_url)
        self.assertContains(response, date)
        self.assertNotContains(response, chapitre_url)

    def test_past_chapitre_in_cours(self):
        """
        Past chapitre in cours links to the chapitre detail view
        """
        self.login_user()
        cours = create_cours(titre='Cours', days=-1)
        past_chapitre = create_chapitre(titre='Chapitre past', cours=cours, days=-1)
        chapitre_url = reverse('cours:chapitre-detail', args=(cours.id, past_chapitre.slug,))
        cours_url = reverse('cours:cours-detail', args=(cours.id,))
        response = self.client.get(cours_url)
        self.assertContains(response, chapitre_url)

    def test_chapitre_from_other_cours(self):
        """
        Chapitre from cours A does not show up on cours B page
        """
        self.login_user()
        cours_a = create_cours(titre='Cours A', days=-1)
        cours_b = create_cours(titre='Cours B', days=-1)
        chapitre = create_chapitre(titre='Chapitre', cours=cours_a, days=-1)
        url = reverse('cours:cours-detail', args=(cours_b.id,))
        response = self.client.get(url)
        self.assertNotContains(response, chapitre.titre)


class ChapitreDetailViewTests(TestCase):

    def login_user(self):
        create_user(username='test', password='password123')
        self.client.login(username='test', password='password123')

    def test_future_chapitre(self):
        """
        Future chapitre cannot be viewed
        """
        self.login_user()
        cours = create_cours(titre='Cours', days=-1)
        future_chapitre = create_chapitre(titre='Chapitre future', cours=cours, days=1)
        url = reverse('cours:chapitre-detail', args=(cours.id, future_chapitre.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_chapitre(self):
        """
        Past chapitre can be viewed
        """
        self.login_user()
        cours = create_cours(titre='Cours', days=-1)
        past_chapitre = create_chapitre(titre='Chapitre past', cours=cours, days=-1)
        url = reverse('cours:chapitre-detail', args=(cours.id, past_chapitre.slug,))
        response = self.client.get(url)
        self.assertContains(response, past_chapitre.titre)
