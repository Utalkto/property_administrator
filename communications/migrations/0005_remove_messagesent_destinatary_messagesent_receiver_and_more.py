# Generated by Django 4.0.4 on 2022-05-19 17:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_units_unit'),
        ('tickets', '0011_rename_created_by_ticketcomments_ticket'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communications', '0004_messagesent_via'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messagesent',
            name='destinatary',
        ),
        migrations.AddField(
            model_name='messagesent',
            name='receiver',
            field=models.CharField(default='tenant', max_length=80),
        ),
        migrations.AddField(
            model_name='messagesent',
            name='supplier',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.suppliers'),
        ),
        migrations.AddField(
            model_name='messagesent',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='properties.tenants'),
        ),
        migrations.AddField(
            model_name='messagesent',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='messagesent',
            name='sent_by',
            field=models.CharField(default='user', max_length=80),
        ),
    ]