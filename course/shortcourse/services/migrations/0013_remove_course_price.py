# Generated by Django 4.0.3 on 2022-04-26 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_remove_course_price_currency_alter_course_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='price',
        ),
    ]
