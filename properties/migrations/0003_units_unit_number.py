# Generated by Django 4.0.4 on 2022-05-26 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='unit_number',
            field=models.IntegerField(default=0),
        ),
    ]