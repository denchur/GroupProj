# Generated by Django 3.2 on 2023-05-25 12:29

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
                    ('user', 'user'),
                    ('admin', 'admin'),
                    ('moderator', 'moderator'),
                ],
                default='user',
                max_length=20,
            ),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(
                fields=('username', 'email'), name='unique_username_email'
            ),
        ),
    ]
