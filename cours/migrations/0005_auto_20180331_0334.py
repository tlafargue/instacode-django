# Generated by Django 2.0.3 on 2018-03-31 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0004_auto_20180331_0333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exercice',
            old_name='album',
            new_name='Exo',
        ),
    ]
