# Generated by Django 4.0.3 on 2022-05-17 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0025_alter_like_dislike_dislike_alter_like_dislike_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like_dislike',
            name='dislike',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='like_dislike',
            name='like',
            field=models.IntegerField(null=True),
        ),
    ]
