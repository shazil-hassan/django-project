# Generated by Django 4.0.3 on 2022-05-17 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0028_alter_like_dislike_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like_dislike',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.review'),
        ),
    ]