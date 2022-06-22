# Generated by Django 4.0.4 on 2022-06-22 12:50

from django.db import migrations, models
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0024_organization_password_test_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='password_test',
        ),
        migrations.AddField(
            model_name='organization',
            name='email_password',
            field=models.BinaryField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='email_username',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='key',
            field=models.BinaryField(default=None, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='clients_access',
            field=register.models.IntKeyJSONField(default=dict, validators=[register.models.outer_json_is_object, register.models.outer_json_is_object]),
        ),
    ]