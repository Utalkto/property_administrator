# Generated by Django 3.2.12 on 2022-05-26 15:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.CharField(default='<function uuid4 at 0x7ffa6d602670>', max_length=120, primary_key=True, serialize=False)),
                ('product', models.CharField(default=None, max_length=120, null=True)),
                ('characteristics', models.CharField(default=None, max_length=120, null=True)),
                ('price', models.CharField(default=None, max_length=120, null=True)),
                ('status', models.CharField(default=None, max_length=120, null=True)),
                ('ice_cream', models.CharField(default=None, max_length=120, null=True)),
                ('drink', models.CharField(default=None, max_length=120, null=True)),
                ('dough', models.CharField(default=None, max_length=120, null=True)),
                ('email', models.EmailField(default=None, max_length=254, null=True)),
                ('email2', models.EmailField(default=None, max_length=254, null=True)),
                ('date_time_order', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
