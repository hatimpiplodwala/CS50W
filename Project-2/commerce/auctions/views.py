from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *

categories=["All", "Electronics", "Art", "Books", "Clothing", "Games", "Other"]
selectable=categories.copy()
selectable.remove("All")

def checkbidprice():
    listings=Listing.objects.filter(status=1)
    for listing in listings:
        maxbid=Bid.objects.filter(item_id=listing.id).order_by("-amount").first()
        if not maxbid:
            listing.currentprice=listing.startingbid
        elif listing.currentprice != maxbid.amount:
            listing.currentprice=maxbid.amount
            
        listing.save()
    
def index(request):
    checkbidprice()
    return render(request, "auctions/index.html",{
            "activeitems": Listing.objects.filter(status=1),
    })

def category(request):
    checkbidprice()
    if request.method=="POST":
        category=request.POST["category"]
        
        if category == "All":
            return redirect("/")
        
        elif category not in categories:
            return render(request, "auctions/categories.html",{
                "message":"Requested category not found",
                "categories": categories
            })
            
        else:
            return render(request, "auctions/index.html",{
                "activeitems": Listing.objects.filter(status=1 ,category=category),
            })
        
    else: 
        return render(request, "auctions/categories.html",{
            "categories": categories
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

@login_required(redirect_field_name=None, login_url="/login")
def createlisting(request):
    if request.method=="POST":
        user_id = User.objects.get(username=request.user.username)
        title=request.POST["title"]
        description = request.POST["description"]
        if len(description) > 100:
            return render(request, "auctions/create.html",{
                "selectable": selectable,
                "message":"Description exceeded 100 characters"
            })
            
        startbid= request.POST["startbid"]
        if not startbid.isnumeric() or float(startbid) < 0:
            return render(request, "auctions/create.html",{
                "selectable": selectable,
                "message":"Price fields should be numeric and greater than 0"
            })
        
        imageurl = request.POST["imageurl"]
        category=request.POST["category"]
        if category not in selectable:
            return render(request, "auctions/create.html",{
                "selectable": selectable,
                "message":"Entered category is invalid"
            })
            
        status=1 #active listing
        listing = Listing(user_id=user_id, title=title, description=description, startingbid=float(startbid),
                            currentprice=float(startbid), imageurl=imageurl, category=category, status=status)
        listing.save()
        
    return render(request, "auctions/create.html",{
        "selectable": selectable,
    })
    
def listing_view(request, i):
    checkbidprice()
    listing=Listing.objects.get(id=i)
    if listing.status == 0:
        return render(request, "auctions/listing.html", {
            "message": "Listing is closed"
        })
        
    bidcount=Bid.objects.filter(item_id=i).count()
    maxbid=Bid.objects.filter(item_id=i).order_by("-amount").first()
    comments=Comment.objects.filter(item_id=i)
    if request.user.is_authenticated:
        onwatchlist=Watchlist.objects.filter(item_id=i).filter(user_id=User.objects.get(username=request.user.username))
    else:
        onwatchlist=None
    return render(request, "auctions/listing.html", {
        "listing": listing, "bidsmade": bidcount, "highestbider": maxbid,
        "comments": comments, "onwatchlist": onwatchlist
    })

@login_required(redirect_field_name=None, login_url="/login")
def makebid(request, i):
    if request.method=="POST":
        user_id=User.objects.get(username=request.user.username)
        comments=Comment.objects.filter(item_id=i)
        bidcount=Bid.objects.filter(item_id=i).count()
        onwatchlist=Watchlist.objects.filter(item_id=i).filter(user_id=user_id)
        
        listing=Listing.objects.get(id=i)
        if listing.status == 0:
            return render(request, "auctions/listing.html", {
                "message": "Listing is closed"
            })
        
        userbid=request.POST["bid"]
        maxbid=Bid.objects.filter(item_id=i).order_by("-amount").first()
        
        if maxbid:
            if not userbid.isnumeric() or float(userbid) < maxbid.amount:
                return render(request, "auctions/listing.html", {
                    "message":"Invalid bid amount. Must be greater than highest bid.",
                    "listing": listing, "bidsmade": bidcount, "highestbider": maxbid,
                    "comments": comments, "onwatchlist": onwatchlist
                })
                
        else:
            if not userbid.isnumeric() or float(userbid) < listing.startingbid:
                return render(request, "auctions/listing.html", {
                    "message":"Invalid bid amount. Must be greater than starting bid.",
                    "listing": listing, "bidsmade": bidcount, "highestbider": maxbid,
                    "comments": comments, "onwatchlist": onwatchlist
                })
        
        addbid = Bid(user_id=user_id, item_id=listing, amount=userbid)
        addbid.save()
        listing.currentprice=userbid
        listing.save()
        
        return redirect(f"/listing/{i}")
    
    else:
        return redirect("/")

@login_required(redirect_field_name=None, login_url="/login")
def alterwatchlist(request, i):
    if request.method=="POST":
        user_id=User.objects.get(username=request.user.username)
        listing=Listing.objects.get(id=i)
        
        onwatchlist=Watchlist.objects.filter(item_id=i).filter(user_id=user_id)
        if not onwatchlist:
            addwatch=Watchlist(user_id=user_id, item_id=listing)
            addwatch.save()
        else:
            Watchlist.objects.filter(item_id=i).filter(user_id=user_id).delete()
        
        return redirect(f"/listing/{i}")
    
    else:
        return redirect("/")

@login_required(redirect_field_name=None, login_url="/login")
def addcomment(request, i):
    if request.method=="POST":
        user_id=User.objects.get(username=request.user.username)
        maxbid=Bid.objects.filter(item_id=i).order_by("-amount").first()
        bidcount=Bid.objects.filter(item_id=i).count()
        onwatchlist=Watchlist.objects.filter(item_id=i).filter(user_id=user_id)
            
        listing=Listing.objects.get(id=i)
        if listing.status == 0:
            return render(request, "auctions/listing.html", {
                "message": "Listing is closed"
            })
            
        usercomment=request.POST["comment"]
        comments=Comment.objects.filter(item_id=i)
        
        if len(usercomment) > 100:
            return render(request, "auctions/listing.html", {
                "message":"Comment exceeded 100 characters",
                "listing": listing, "bidsmade": bidcount, "highestbider": maxbid,
                "comments": comments, "onwatchlist": onwatchlist
            })
        elif len(usercomment) == 0:
            return render(request, "auctions/listing.html", {
                "message":"No comment provided",
                "listing": listing, "bidsmade": bidcount, "highestbider": maxbid,
                "comments": comments, "onwatchlist": onwatchlist
            })
        
        addcomment=Comment(user_id=user_id, item_id=listing, comment=usercomment)
        addcomment.save()
        
        return redirect(f"/listing/{i}")
    
    else:
        return redirect("/")

@login_required(redirect_field_name=None, login_url="/login")
def closebid(request, i):
    if request.method=="POST":
        listing=Listing.objects.get(id=i)
        listing.status=0
        listing.save()
        
        maxbid=Bid.objects.filter(item_id=i).order_by("-amount").first()
        if maxbid:
            won=Winner(user_id=maxbid.user_id, item_id=listing)
            won.save()
            
        return redirect("/")
    
    else:
        return redirect("/")
  
@login_required(redirect_field_name=None, login_url="/login")  
def viewwatchlist(request):
    if request.method=="POST":
        user_id=User.objects.get(username=request.user.username)
        i=request.POST["itemtochange"]
        listing=Listing.objects.get(id=i)
        
        onwatchlist=Watchlist.objects.filter(item_id=i).filter(user_id=user_id)
        if not onwatchlist:
            addwatch=Watchlist(user_id=user_id, item_id=listing)
            addwatch.save()
        else:
            Watchlist.objects.filter(item_id=i).filter(user_id=user_id).delete()
        
        return redirect("/viewwatchlist")
    else:
        user_id=User.objects.get(username=request.user.username)
        itemswatchlisted=Watchlist.objects.filter(user_id=user_id)
        watchlistdetails=[]
        for i in itemswatchlisted:
            listing=Listing.objects.get(id=i.item_id.id)
            highestbider=Bid.objects.filter(item_id=i.item_id.id).order_by("-amount").first()
            bidcount=Bid.objects.filter(item_id=i.item_id.id).count()
            watchlistdetails.append([listing, highestbider, bidcount])
            
        return render(request, "auctions/watchlist.html", {
            "watchlist": watchlistdetails
        })

@login_required(redirect_field_name=None, login_url="/login")   
def viewwinsbids(request):
    
    user_id=User.objects.get(username=request.user.username)
    mybids=Bid.objects.filter(user_id=user_id)
    mywins=Winner.objects.filter(user_id=user_id)
    biddetails=[]
    windetails=[]
    
    for i in mywins:
        listing=Listing.objects.get(id=i.item_id.id)
        mybid=Bid.objects.filter(item_id=i.item_id.id).get(user_id=user_id).amount
        windetails.append([listing, mybid])
    
    for i in mybids:
        listing=Listing.objects.get(id=i.item_id.id)
        highestbider=Bid.objects.filter(item_id=i.item_id.id).order_by("-amount").first()
        mybid=Bid.objects.filter(item_id=i.item_id.id).get(user_id=user_id).amount
        bidcount=Bid.objects.filter(item_id=i.item_id.id).count()
        biddetails.append([listing, highestbider, bidcount, mybid])
            
    return render(request, "auctions/winsandbids.html", {
            "bidlist": biddetails,
            "winlist": windetails
    })
    
def viewmylistings(request):
    user_id = User.objects.get(username=request.user.username)
    listings = Listing.objects.filter(user_id=user_id)
    
    listingdetails=[]
    for i in listings:
        highestbider=Bid.objects.filter(item_id=i.id).order_by("-amount").first()
        bidcount=Bid.objects.filter(item_id=i.id).count()
        listingdetails.append([i, highestbider, bidcount])
    
    return render(request, "auctions/mylisting.html", {
            "listinglist": listingdetails
        })