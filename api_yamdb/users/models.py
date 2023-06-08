from django.db import models
from django.contrib.auth.models import AbstractUser


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES_CHOICES = {
    (USER, 'Пользователь'),
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
}


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, blank=False, null=False
    )
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False
    )
    role = models.CharField(
        max_length=20,
        blank=True,
        choices=ROLES_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        max_length=1000,
        blank=True,
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
