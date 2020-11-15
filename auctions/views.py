from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auctions, Comments, Bids, AuctionsForm, BidsForm, CommentsForm


def index(request):

    auctionsList = Auctions.objects.filter(active=True).order_by('pk').reverse()
    noticeList = noticeAuctions(request.user)

    return render(request, "auctions/index.html", {
        "listings": auctionsList,
        "noticeList": noticeList,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    
    form = AuctionsForm()

    if request.method == "GET":

        return render(request, 'auctions/createListing.html', {
            "form": form
        })

    else:

        formPosted = AuctionsForm(request.POST)
        new_auction = formPosted.save()

        user = request.user
        user.auctions_owner.add(new_auction)

        return HttpResponseRedirect(reverse("index"))

def auctionPage(request, auctionID, token=1, message=None):

    if request.method == "GET" or token != 1:

        listing = Auctions.objects.get(pk=auctionID)
        owner = User.objects.filter(auctions_owner=auctionID).first()
        bidMax = listing.bids_in_auction.order_by('value').last()
        
        user = request.user

        anonymous = False

        if user.is_anonymous:
            anonymous = True
            interest = False
        else:
            interest = user.auctions_interest.filter(pk=auctionID)

        if user == owner:
            ownerIn = True
        else:
            ownerIn = False
        
        if interest:
            interest = True
        else:
            interest = False

        list_comments = getCommentsInAuction(auctionID)[::-1]

        return render(request, 'auctions/auctionPage.html', {
            "listing": listing,
            "owner": owner,
            "bidMax": bidMax,
            "interest": interest,
            "auctionID": auctionID,
            "message": message,
            "ownerIn": ownerIn,
            "anonymous": anonymous,
            "comments": list_comments ,
            "bidForm": BidsForm(),
            "commentForm": CommentsForm()
        })

    bid = BidsForm(request.POST)

    if bid == None:
        return None

    new_bid = bid.save()

    listing = Auctions.objects.get(pk=auctionID)
    bidMax = listing.bids_in_auction.order_by('value').last()

    if new_bid.value <= listing.first_bid:
        new_bid.remove()
        return auctionPage(request, auctionID, 2, "The bid must be grater than the first bid!")

    if bidMax:
        if new_bid.value <= bidMax.value:
            new_bid.remove()
            return auctionPage(request, auctionID, 2, "The bid must be grater than the current bid!")

    user = request.user
    if user.is_anonymous:
        return auctionPage(request, auctionID, 2, "You must log in to bid!")
    user.bids_owner.add(new_bid)

    listing.bids_in_auction.add(new_bid)

    return auctionPage(request, auctionID, 2, "Bidded!")

def addRemoveWatchList(request, auctionID, mode):

    if request.method == "POST":
        return auctionPage(request, auctionID)
    
    if mode == "add":
        
        user = request.user
        listing = Auctions.objects.get(pk=auctionID)
        user.auctions_interest.add(listing)

        return auctionPage(request, auctionID, 2, "Added!")

    else:
        user = request.user
        listing = Auctions.objects.get(pk=auctionID)
        user.auctions_interest.remove(listing)

        return auctionPage(request, auctionID, 2, "Removed!")

def finishListing(request, auctionID):
    
    listing = Auctions.objects.get(pk=auctionID)
    bidMax = listing.bids_in_auction.order_by('value').last()

    if bidMax == None:
        
        listing.active = False
        listing.noticed = True
        listing.save()        

        return render(request, 'auctions/finishNotBid.html', {
            "listing": listing
        })

    pk = bidMax.pk
    winner = User.objects.get(bids_owner=pk)

    listing.active = False
    listing.save()        

    return render(request, 'auctions/finishAuction.html', {
        "winner": winner,
        "bidMax": bidMax,
        "listing": listing,
        "auctionID": auctionID
    })

def noticeAuctions(user):

    auctionsToNotice = Auctions.objects.filter(active=False).filter(noticed=False)

    if auctionsToNotice == None:
        return None

    auctionsList = []

    for auction in auctionsToNotice:
        auctionArray = []
        bidMax = auction.bids_in_auction.order_by('value').last()
        if user == User.objects.get(bids_owner=bidMax.pk) and not auction == None:
            auctionArray.append(auction)
            auctionArray.append(bidMax)
            auction.noticed = True
            auction.save() 
            auctionsList.append(auctionArray)
    
    return auctionsList
    
def makeComment(request, auctionID):

    if request.method == "POST":

        comment = CommentsForm(request.POST)

        if comment == None:
            return HttpResponse("error")
        
        new_comment = comment.save()

        listing = Auctions.objects.get(pk=auctionID)
        
        user = request.user
        if user.is_anonymous:
            return auctionPage(request, auctionID, 2, "You must log in to comment!")
        user.comments_owner.add(new_comment)

        listing.comments_in_auction.add(new_comment)

        return auctionPage(request, auctionID, 2, "Commented!")

def getCommentsInAuction(auctionID):

    list_comments = []

    listing = Auctions.objects.get(pk=auctionID)
    comments = listing.comments_in_auction.all()

    for comment in comments:
        owner = User.objects.get(comments_owner=comment)
        fullComment = []
        fullComment.append(comment)
        fullComment.append(owner) 
        list_comments.append(fullComment)    

    return list_comments

def watchList(request):
    
    user = request.user

    interests = user.auctions_interest.all().filter(active=True).order_by('pk').reverse()

    return render(request, "auctions/wacthList.html", {
        "listings": interests,
    })

def categories(request):
    
    if request.method == "GET":

        listings = Auctions.objects.all().filter(active=True)
        all_categories = []


        for listing in listings:
            if listing.category != None:
                all_categories.append(listing.category)

        return render(request, "auctions/categories.html", {
            "categories": all_categories,
        })

def categoryPage(request, category):
    
    listings = Auctions.objects.filter(active=True, category=category)

    return render(request, 'auctions/categoryPage.html', {
        "listings": listings,
        "category": category,
    })

        