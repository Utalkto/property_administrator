# Generated by Django 4.0.4 on 2022-05-16 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('properties', '0001_initial'),
        ('candidates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='property_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='candidate',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.units'),
        ),
    ]