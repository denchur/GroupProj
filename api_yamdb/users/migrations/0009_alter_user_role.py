# Generated by Django 3.2 on 2023-05-29 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')], default='user', max_length=20),
        ),
    ]
