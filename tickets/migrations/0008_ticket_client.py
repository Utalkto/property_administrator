# Generated by Django 4.0.4 on 2022-07-11 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0057_alter_customuser_clients_access'),
        ('tickets', '0007_suppliers_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='register.organizationclient'),
        ),
    ]
