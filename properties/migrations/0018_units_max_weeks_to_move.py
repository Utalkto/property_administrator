# Generated by Django 4.0.4 on 2022-06-14 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0017_units_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='max_weeks_to_move',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
