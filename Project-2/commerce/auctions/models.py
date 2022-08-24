from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listedby")
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    imageurl = models.URLField()
    category = models.CharField(max_length=20)
    startingbid = models.FloatField()
    currentprice=models.FloatField()
    status = models.IntegerField()
    
class Bid(models.Model):
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="itembidon")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bider")
    amount = models.FloatField()
    
class Comment(models.Model):
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="itemcommentedon")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=100)
    
class Winner(models.Model):
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="itembought")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    
class Watchlist(models.Model):
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="itemwatchlist")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlistedby")
