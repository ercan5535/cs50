from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import User, Category, Listings, Comment, Bid

def listing(request, id):
    list_obj = Listings.objects.get(pk=id)
    comments = list_obj.listing_comment.all()
    isListingInWatchlist = request.user in list_obj.watchlist.all()

    return render(request, "auctions/listing.html", {
        "listing":list_obj,
        "isListingInWatchlist":isListingInWatchlist,
        "comments": comments    
    })

def make_bid(request, id):
    bid_amount = request.POST["bid_amount"]
    current_listing = Listings.objects.get(pk=id)
    bids_of_listing = current_listing.listing_bid.all()
    if bid_amount:
        bid_amount = float(bid_amount)
        # Check for first bid
        if not bids_of_listing and bid_amount > current_listing.initial_price:
            # Update Listing
            current_listing.bid_count += 1
            current_listing.current_amount = bid_amount
            current_listing.save()

            # Create Bid
            new_bid = Bid(
                owner = request.user,
                listing = current_listing,
                amount = bid_amount
            )
            new_bid.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        
        # Check amount is bigger than last bid's amount
        if bid_amount > bids_of_listing.last().amount:
            # Update Listing
            current_listing.bid_count += 1
            current_listing.current_amount = bid_amount
            current_listing.save()

            # Create Bid
            new_bid = Bid(
                owner = request.user,
                listing = current_listing,
                amount = bid_amount
            )
            new_bid.save()
            return HttpResponseRedirect(reverse("listing", args=(id,)))

        # Return Error
        return ValidationError("Bid amount should be bigger than current amount")
    return

def close_listing(request, id):
    # Get Current listing and Last Bid owner
    current_listing = Listings.objects.get(pk=id)
    last_bid_owner = current_listing.listing_bid.last().owner

    # Close Listing and Update winner
    current_listing.winner = last_bid_owner
    current_listing.isActive = False

    # Save Listing
    current_listing.save()

    return HttpResponseRedirect(reverse("listing", args=(id,)))

def add_comment(request, id):
    comment_message = request.POST["comment_message"]
    current_listing = Listings.objects.get(pk=id)
    current_user = request.user

    comment = Comment(
        author=current_user,
        listing=current_listing,
        message=comment_message
    )

    comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def display_watchlist(request):
    current_user = request.user
    listings_in_watchlist = current_user.listing_watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": listings_in_watchlist
    })

def add_watchlist(request, id):
    listing_obj = Listings.objects.get(pk=id)
    current_user = request.user
    listing_obj.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def remove_watchlist(request, id):
    listing_obj = Listings.objects.get(pk=id)
    current_user = request.user
    listing_obj.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def index(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        active_listings = Listings.objects.filter(isActive = True)
        return render(request, "auctions/index.html",{
            "listings": active_listings,
            "categories": all_categories
        })

    else:
        selected_category = request.POST["category"]
        if selected_category == "All":
            active_listings = Listings.objects.filter(isActive=True)
        else:
            active_listings = Listings.objects.filter(
                isActive=True,
                category=Category.objects.get(categoryName=selected_category)
            )

        all_categories = Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings": active_listings,
            "categories": all_categories
        })

def create_listing(request):
    all_categories = Category.objects.all()
    if request.method == "GET":
        return render(request, "auctions/create.html",{
            "categories": all_categories
        })
    
    else:
        # Get the data from the form
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageUrl"]
        price = request.POST["price"]
        category = Category.objects.get(categoryName = request.POST["category"])

        current_user = request.user
        # Create a new listing object
        new_listing = Listings(
            title=title,
            description=description,
            imageUrl=imageurl,
            initial_price=float(price),
            category=category,
            owner=current_user
        )
        # Insert the object in database
        new_listing.save()

        # Redirect to index page
        return HttpResponseRedirect(reverse("index"))
    
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
