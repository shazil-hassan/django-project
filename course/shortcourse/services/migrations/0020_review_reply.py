# Generated by Django 4.0.3 on 2022-05-11 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0019_alter_review_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='services.review'),
        ),
    ]
