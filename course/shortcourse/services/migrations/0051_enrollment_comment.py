# Generated by Django 4.0.5 on 2022-08-01 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0050_alter_course_id_alter_course_price_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='comment',
            field=models.CharField(max_length=200, null=True),
        ),
    ]