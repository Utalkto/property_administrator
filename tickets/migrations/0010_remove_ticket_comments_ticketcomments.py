# Generated by Django 4.0.4 on 2022-05-19 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0009_ticket_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='comments',
        ),
        migrations.CreateModel(
            name='TicketComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.ticket')),
            ],
        ),
    ]
