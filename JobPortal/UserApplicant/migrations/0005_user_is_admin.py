# Generated by Django 5.0.7 on 2024-07-27 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApplicant', '0004_jobseeker_profile_about_jobseeker_profile_insta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]