# Generated by Django 4.0.4 on 2022-07-20 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_form_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='number_of_views',
            field=models.IntegerField(default=0),
        ),
    ]
