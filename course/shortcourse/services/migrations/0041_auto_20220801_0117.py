# Generated by Django 3.1.1 on 2022-07-31 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0040_auto_20220801_0000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cnic',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='educational_background',
            field=models.TextField(),
        ),
    ]