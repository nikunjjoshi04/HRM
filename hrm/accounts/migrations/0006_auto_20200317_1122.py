# Generated by Django 3.0.4 on 2020-03-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_candidate_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]
