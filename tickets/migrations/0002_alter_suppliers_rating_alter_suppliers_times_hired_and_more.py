# Generated by Django 4.0.4 on 2022-05-27 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suppliers',
            name='rating',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='suppliers',
            name='times_hired',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='suppliers',
            name='work_area',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tickets.supplierworkarea'),
        ),
    ]
