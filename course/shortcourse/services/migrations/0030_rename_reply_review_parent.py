# Generated by Django 4.0.3 on 2022-05-17 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0029_alter_like_dislike_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='reply',
            new_name='parent',
        ),
    ]
