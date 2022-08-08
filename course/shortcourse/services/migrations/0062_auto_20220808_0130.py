# Generated by Django 3.1.1 on 2022-08-07 20:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0061_assignment_due_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='FAQ',
            new_name='Faqs',
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='apply_date',
            field=models.DateField(default=datetime.date(2022, 8, 8)),
        ),
        migrations.AlterField(
            model_name='enrollment',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]