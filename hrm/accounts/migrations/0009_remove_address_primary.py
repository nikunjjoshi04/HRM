# Generated by Django 3.0.4 on 2020-03-19 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_candidate_experience'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='primary',
        ),
    ]
