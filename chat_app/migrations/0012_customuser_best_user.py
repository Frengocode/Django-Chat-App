# Generated by Django 5.0.4 on 2024-04-21 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0011_alter_customuser_profile_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='best_user',
            field=models.BooleanField(default=False),
        ),
    ]