# Generated by Django 3.1.1 on 2022-07-31 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0045_service_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='enrollment_start_date',
            field=models.DateField(null=True),
        ),
    ]