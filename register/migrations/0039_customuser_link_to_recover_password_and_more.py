# Generated by Django 4.0.4 on 2022-06-29 13:09

from django.db import migrations, models
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0038_alter_customuser_clients_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='link_to_recover_password',
            field=models.CharField(default=None, max_length=26, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='time_recover_link_creation',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]