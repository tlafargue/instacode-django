# Generated by Django 2.0.3 on 2018-04-04 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cours', '0008_profile_interest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(null=True),
        ),
    ]
