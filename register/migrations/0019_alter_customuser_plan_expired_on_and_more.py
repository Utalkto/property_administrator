# Generated by Django 4.0.4 on 2022-05-19 17:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0018_alter_customuser_plan_expired_on_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='plan_expired_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 26, 13, 46, 55, 663194)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 19, 13, 46, 55, 663194)),
        ),
    ]
