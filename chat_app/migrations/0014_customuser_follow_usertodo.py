# Generated by Django 5.0.4 on 2024-04-21 19:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0013_remove_customuser_best_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='follow',
            field=models.ManyToManyField(related_name='subscribe_field', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('to_do', models.CharField(max_length=1000)),
                ('img', models.ImageField(upload_to='to_do_img/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
