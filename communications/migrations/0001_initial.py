# Generated by Django 4.0.4 on 2022-05-25 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_sent', models.DateTimeField()),
                ('message', models.TextField(default='')),
                ('receiver', models.CharField(default='tenant', max_length=80)),
                ('subject', models.CharField(max_length=120, null=True)),
                ('sent_by', models.CharField(default='user', max_length=80)),
                ('via', models.CharField(default='', max_length=50)),
            ],
        ),
    ]
