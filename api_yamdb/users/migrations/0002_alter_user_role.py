# Generated by Django 3.2 on 2023-05-24 15:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(
                blank=True,
                choices=[
                    ('admin', 'admin'),
                    ('moderator', 'moderator'),
                    ('user', 'user'),
                ],
                default='user',
                max_length=20,
            ),
        ),
    ]
