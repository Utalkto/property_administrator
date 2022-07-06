# Generated by Django 4.0.4 on 2022-07-06 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0025_remove_property_create_by_remove_tenants_create_by_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unit',
            name='pet_fee',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='pet_friendly',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='pet_typee',
        ),
        migrations.RemoveField(
            model_name='unit',
            name='pets_living',
        ),
        migrations.AlterField(
            model_name='unit',
            name='has_pet',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='number_of_pets',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.DeleteModel(
            name='PetType',
        ),
    ]
