# Generated by Django 5.0.7 on 2024-08-05 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admincontrol', '0002_alter_contact_main_created_at'),
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frequently_asked',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contact.contact')),
            ],
        ),
    ]
