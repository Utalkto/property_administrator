# Generated by Django 3.2.12 on 2022-05-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watson', '0008_alter_product_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(default='3fc03c21-2fe6-4825-90e1-61d6fba642a2', max_length=120, primary_key=True, serialize=False),
        ),
    ]