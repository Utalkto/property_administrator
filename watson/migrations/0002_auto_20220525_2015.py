# Generated by Django 3.2.12 on 2022-05-25 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watson', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='extra_toppings',
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(default='5e8438e9-9a84-4ca7-b8b6-db8c8d7643eb', max_length=120, primary_key=True, serialize=False),
        ),
    ]
