# Generated by Django 4.0.4 on 2022-05-13 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0022_alter_customuser_plan_expired_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='plan_expired_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 20, 12, 13, 5, 651964)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 13, 12, 13, 5, 651964)),
        ),
    ]
