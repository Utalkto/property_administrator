# Generated by Django 4.0.4 on 2022-05-27 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watson', '0002_alter_product_product_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='email2',
        ),
        migrations.AddField(
            model_name='product',
            name='extra_toppingss',
            field=models.CharField(default=None, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.CharField(default='e4b058a0-3eaf-4164-9f50-1ebcfaa0c026', max_length=120, primary_key=True, serialize=False),
        ),
    ]