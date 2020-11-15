from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm
from django.utils.timezone import now

class Bids(models.Model):
    value = models.DecimalField(max_digits=8, decimal_places=2)

class Comments(models.Model):
    comment_date = models.DateField(default=now, verbose_name='date created')
    content = models.CharField(max_length=256)

class Auctions(models.Model):
    Title = models.CharField(max_length=64)
    image_url = models.URLField(blank=True)
    description = models.CharField(max_length=512)
    category = models.CharField(max_length=128, blank=True)
    auction_date = models.DateField(default=now, verbose_name='date created')
    first_bid = models.DecimalField(max_digits=8, decimal_places=2)
    bids_in_auction = models.ManyToManyField(Bids, blank=True, related_name="auctionBid")
    comments_in_auction = models.ManyToManyField(Comments, blank=True, related_name="auctionComment")
    active = models.BooleanField(default=True)
    noticed = models.BooleanField(default=False)

    def __str__(self):
        return self.Title
    

class User(AbstractUser):
    auctions_owner = models.ManyToManyField(Auctions, blank=True, related_name="auctionOwner")
    auctions_interest = models.ManyToManyField(Auctions, blank=True, related_name="auctionInterested")
    comments_owner = models.ManyToManyField(Comments, blank=True, related_name="commentOwner")
    bids_owner = models.ManyToManyField(Bids, blank=True, related_name="bidOwner")

    def __str__(self):
        return (f"{self.username}")
    

class AuctionsForm(ModelForm):

    class Meta:

        model = Auctions
        fields = ('Title', 'description', 'category', 'image_url', 'first_bid')

class BidsForm(ModelForm):

    class Meta:

        model = Bids
        fields = ('value',)

class CommentsForm(ModelForm):

    class Meta:

        model = Comments
        fields = ('content',)

