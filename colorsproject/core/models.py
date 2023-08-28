from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import time
import uuid
import hashlib


def key_generating():
    x = uuid.uuid4().hex
    hash = hashlib.sha256(x.encode())
    key = hash.hexdigest()
    return key


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        extra_fields.setdefault('is_active', True)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password is not None:
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


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, null=False, unique=True)
    username = models.CharField(max_length=100, null=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    registration_date = models.DateField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username}"


class Session(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='session', null=True)
    key = models.CharField(max_length=64, default=key_generating)
    date = models.BigIntegerField(default=int(time.time()))

    class Meta:
        db_table = 'session'


class Favourite(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='favourite', null=True)
    car = models.ForeignKey('Car', models.SET_NULL, related_name='favourite', null=True)
    date = models.BigIntegerField(default=int(time.time()))

    class Meta:
        db_table = 'favourite'


class Brand(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, related_name='brand', null=True)
    issue_date = models.DateField()

    class Meta:
        db_table = 'brand'


class Car(models.Model):
    color = models.ForeignKey('Color', on_delete=models.SET_NULL, related_name='car', null=True)
    brand = models.ForeignKey('Brand', on_delete=models.SET_NULL, related_name='car', null=True)
    model = models.CharField(max_length=30)
    image = models.ImageField(upload_to='cars/', null=True)

    class Meta:
        db_table = 'car'


class Color(models.Model):
    color_name = models.CharField(unique=True, max_length=6)

    class Meta:
        db_table = 'color'


class Country(models.Model):
    name = models.CharField(unique=True, max_length=50)
    locale = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        db_table = 'country'
