# Generated by Django 4.0.4 on 2022-05-23 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_units_main_tenant_name'),
        ('payments', '0005_status_alter_unitpayments_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitpayments',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.tenants'),
        ),
    ]
