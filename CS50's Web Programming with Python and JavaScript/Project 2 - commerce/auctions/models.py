from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Listings(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    imageUrl = models.CharField(max_length=1000)
    initial_price = models.FloatField()
    isActive = models.BooleanField(default=True)
    bid_count = models.IntegerField(default=0)
    current_amount = models.FloatField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_listing_owner")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_winner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category_listing")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="listing_watchlist")

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment") 
    message = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.author}'s comment on {self.listing}"

class Bid(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_bid")
    amount = models.FloatField()

    def __str__(self):
        return f"{self.owner}'s bid for {self.listing}"





