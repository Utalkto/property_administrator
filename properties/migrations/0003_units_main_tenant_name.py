# Generated by Django 4.0.4 on 2022-05-20 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='main_tenant_name',
            field=models.CharField(default='Homero el griego', max_length=150),
        ),
    ]
