# Generated by Django 4.0.4 on 2022-07-01 17:58

from django.db import migrations
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0051_rename_link_to_active_email_customuser_link_to_activate_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]
