# Generated by Django 4.0.4 on 2022-05-10 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_rename_tenant_units_tenant_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=500)),
                ('link_name', models.CharField(max_length=150)),
                ('link_type', models.CharField(max_length=150)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.units')),
            ],
        ),
    ]
