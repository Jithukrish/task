# Generated by Django 5.0.7 on 2024-08-05 06:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admincontrol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact_main',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
