# Generated by Django 3.0.4 on 2020-03-24 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_address_primary'),
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='candidate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidate_schedule', to='accounts.Candidate'),
        ),
    ]
