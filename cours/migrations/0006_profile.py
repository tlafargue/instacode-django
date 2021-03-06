# Generated by Django 2.0.3 on 2018-04-04 21:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cours', '0005_auto_20180403_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=30)),
                ('birth_date', models.DateField(blank=True)),
                ('first_name', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, upload_to='profile_image')),
                ('solved_exercices', models.ManyToManyField(to='cours.Exercice')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
