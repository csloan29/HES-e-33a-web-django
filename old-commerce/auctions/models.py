from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    id_listing = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=32)
    description = models.TextField()
    image = models.FileField()


class Bid(models.Model):
    # bid id
    # listing id
    # user id
    # bid amount
    pass


class Comments(models.Model):
    # comment id
    # user id
    # listing id
    # comment text
    pass


class WatchedItem(models.Model):
    # user id
    # listing id
    pass


class Category(models.Model):
    # category
    pass
