# Generated by Django 4.0.2 on 2022-07-01 14:41

from django.db import migrations
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0043_alter_customuser_clients_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]
