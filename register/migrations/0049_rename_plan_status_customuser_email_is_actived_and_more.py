# Generated by Django 4.0.4 on 2022-07-01 14:21

from django.db import migrations, models
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0048_alter_customuser_clients_access'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='plan_status',
            new_name='email_is_actived',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='plan_expired_on',
        ),
        migrations.AddField(
            model_name='customuser',
            name='link_to_active_email',
            field=models.CharField(default=None, max_length=35, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='plan_expired_on',
            field=models.DateTimeField(default=register.models.seven_day_hence),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]
