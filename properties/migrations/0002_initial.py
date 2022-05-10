# Generated by Django 4.0.4 on 2022-05-10 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='property_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tenants',
            name='landlord',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tenants',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.units'),
        ),
        migrations.AddField(
            model_name='properties',
            name='landlord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
