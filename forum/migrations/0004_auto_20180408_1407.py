# Generated by Django 2.0.4 on 2018-04-08 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_forum_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='categorie',
            field=models.CharField(choices=[('Forum1', 'Forum1'), ('Archive', 'archive')], max_length=60),
        ),
    ]
