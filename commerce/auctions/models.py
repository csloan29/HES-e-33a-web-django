from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"


class Listing(models.Model):
    owner = models.ForeignKey("User",
                              on_delete=models.CASCADE,
                              related_name="user_listings")
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    starting_price = models.DecimalField(decimal_places=2, max_digits=32)
    description = models.TextField()
    image_url = models.URLField(max_length=256, null=True)
    category = models.ForeignKey("Category",
                                 on_delete=models.SET_NULL,
                                 related_name="listings",
                                 null=True)
    watchers = models.ManyToManyField("User",
                                      related_name="watched_items")

    def __str__(self):
        return f"""{self.owner} {self.active} {self.title}
                {self.starting_price} {self.description}
                {self.image_url}"""


class Bid(models.Model):
    bidder = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_bids")
    bid_listing = models.ForeignKey(
        "Listing", on_delete=models.CASCADE, related_name="listing_bids")
    amount = models.DecimalField(decimal_places=2, max_digits=32)

    def __str__(self):
        return f"{self.bidder} {self.bid_listing} {self.amount}"


class Comment(models.Model):
    commenter = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_comments")
    com_listing = models.ForeignKey(
        "Listing", on_delete=models.CASCADE, related_name="listing_comments")
    text = models.TextField()

    def __str__(self):
        return f"{self.commenter} {self.com_listing} {self.text}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
