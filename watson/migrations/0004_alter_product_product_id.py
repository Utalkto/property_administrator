# Generated by Django 4.0.4 on 2022-05-27 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watson', '0003_useremail_remove_product_email2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(default='f7b8bf2f-3213-4211-8c1a-12caabba1aa2', max_length=120, primary_key=True, serialize=False),
        ),
    ]
