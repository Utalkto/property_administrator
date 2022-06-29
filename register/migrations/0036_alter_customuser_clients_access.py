# Generated by Django 4.0.4 on 2022-06-23 19:01

from django.db import migrations
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0035_alter_customuser_clients_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]