# Generated by Django 3.1.1 on 2022-08-06 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0056_auto_20220806_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]