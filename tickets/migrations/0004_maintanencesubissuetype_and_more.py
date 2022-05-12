# Generated by Django 4.0.4 on 2022-05-12 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_maintanenceissuedescription'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintanenceSubIssueType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_description', models.CharField(max_length=120)),
                ('maintanence_issue_sub_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.maintanenceissuetype')),
            ],
        ),
        migrations.AlterField(
            model_name='maintanenceissuedescription',
            name='maintanence_issue_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.maintanencesubissuetype'),
        ),
    ]
