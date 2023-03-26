from django.db import models
import time
import uuid


def key_generating():
    x = uuid.uuid4().hex
    hash = hashlib.sha256(x.encode())
    key = hash.hexdigest()
    return key


class User(models.Model):
    login = models.CharField(unique=True, max_length=20, blank=False)
    password = models.CharField(max_length=64, blank=False)
    name = models.CharField(max_length=64, blank=False)
    email = models.CharField(unique=True, max_length=64, blank=False)
    registration_date = models.BigIntegerField(default=int(time.time()))
    last_signin_date = models.BigIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'user'


class Session(models.Model):
    user = models.ForeignKey('User', models.SET_NULL, related_name='session', null=True)
    key = models.CharField(max_length=64, default=key_generating)
    date = models.BigIntegerField(default=int(time.time()))

    class Meta:
        db_table = 'session'


class Favourite(models.Model):
    user = models.ForeignKey('User', models.SET_NULL, related_name='favourite', null=True)
    car = models.ForeignKey('Car', models.SET_NULL, related_name='favourite', null=True)
    date = models.BigIntegerField(default=int(time.time()))

    class Meta:
        db_table = 'favourite'


class Brand(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey('Country', models.SET_NULL, related_name='brand', null=True)
    issue_date = models.DateField()

    class Meta:
        db_table = 'brand'


class Car(models.Model):
    color = models.ForeignKey('Color', models.SET_NULL, related_name='car', null=True)
    brand = models.ForeignKey('Brand', models.SET_NULL, related_name='car', null=True)
    model = models.CharField(max_length=30)

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
