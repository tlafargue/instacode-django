# Generated by Django 2.0.4 on 2018-05-13 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0018_auto_20180513_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='city',
            new_name='ville',
        ),
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Homme', 'Homme'), ('Femme', 'Femme'), ('Autre', 'Autre')], max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='pays',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]