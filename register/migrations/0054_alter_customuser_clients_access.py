# Generated by Django 4.0.4 on 2022-07-04 15:10

from django.db import migrations
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0053_organization_twilio_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]