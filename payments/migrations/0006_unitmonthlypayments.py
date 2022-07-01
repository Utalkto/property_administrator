# Generated by Django 4.0.4 on 2022-06-14 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0016_remove_units_availability'),
        ('payments', '0005_merge_20220602_0926'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitMonthlyPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=120)),
                ('amount_to_pay', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pay_on_time', models.BooleanField()),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.units')),
            ],
        ),
    ]
