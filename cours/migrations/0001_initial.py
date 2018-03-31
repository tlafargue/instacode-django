# Generated by Django 2.0.3 on 2018-03-31 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=100)),
                ('video', models.CharField(max_length=500)),
                ('text', models.CharField(max_length=5000)),
                ('Photo', models.FileField(upload_to='')),
                ('is_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom_Exo', models.CharField(max_length=100)),
                ('Choix_multiple', models.BooleanField(default=False)),
                ('Enonce', models.CharField(max_length=5000)),
                ('Reponse', models.CharField(max_length=5000)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cours.Cours')),
            ],
        ),
    ]
