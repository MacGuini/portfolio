# Generated by Django 5.0.2 on 2024-02-13 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_verification_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
