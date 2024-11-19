from django.contrib.auth.models import User, AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from .utils import generate_file_id, user_directory_path


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Уникальное имя
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Уникальное имя
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Files(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Пользователь'
    )
    file = models.FileField(upload_to=user_directory_path, verbose_name='Файл')
    name = models.CharField(max_length=255, verbose_name='Имя')
    file_id = models.CharField(max_length=10, default=generate_file_id, unique=True)

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        unique_together = ('user', 'file_id')

    def __str__(self):
        return self.name


