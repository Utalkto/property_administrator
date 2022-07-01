# Generated by Django 4.0.4 on 2022-07-01 17:59

from django.db import migrations, models
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0052_alter_customuser_clients_access'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='twilio_number',
            field=models.CharField(default=None, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]
