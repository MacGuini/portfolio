# Generated by Django 5.0.2 on 2024-02-12 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_is_valid_profile_is_approved'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='email_Valid',
            new_name='email_valid',
        ),
    ]
