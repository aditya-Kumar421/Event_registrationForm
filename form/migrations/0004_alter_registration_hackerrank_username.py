# Generated by Django 5.0 on 2024-08-05 05:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_alter_registration_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='hackerRank_username',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]