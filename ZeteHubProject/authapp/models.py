from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom manager for UserCredentials
class UserCredentialsManager(BaseUserManager):
    def create_user(self, username, phone_number, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, phone_number=phone_number, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)  # This takes care of hashing the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, phone_number, first_name, last_name, password, **extra_fields)

# UserCredentials model
class UserCredentials(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)  # This is required by Django's auth system
    is_staff = models.BooleanField(default=False)  # This is required by Django's auth system

    # Required for Django's user model
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    objects = UserCredentialsManager()

    def __str__(self):
        return self.username
