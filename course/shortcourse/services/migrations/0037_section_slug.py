# Generated by Django 3.1.1 on 2022-07-31 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0036_auto_20220731_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]
