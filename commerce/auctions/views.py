import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from annoying.functions import get_object_or_None

from .forms import ListingForm
from .models import User, Listing, Bid, Comment, Category


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))

        return render(request, "auctions/login.html", {
            "message": "Invalid username and/or password."
        })

    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))

    return render(request, "auctions/register.html")


def index(request):
    listings = Listing.objects.filter(active=True)
    # get highest price if bids exist
    for listing in listings:
        # starting with starting price
        highest_bid = listing.starting_price
        bids = listing.listing_bids.all()
        if bids:
            # find max of bid amounts
            highest_bid = max(bid.amount for bid in bids)
        setattr(listing, "price", highest_bid)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def get_listing(request, listing_id):
    listing_obj = get_object_or_None(Listing, id=listing_id)
    if listing_obj is None:
        return render(request, "auctions/not_found.html", {
            "errMsg": "Listing Not Found"
        })

    # get all necessary data for listing page
    bids = listing_obj.listing_bids.all()
    comments = listing_obj.listing_comments.all()

    # preset data
    user = None
    user_owned = False
    watched_items = None
    highest_bid_amount = listing_obj.starting_price
    minimum_bid_amount = listing_obj.starting_price
    user_highest_bid = False

    # if there is a current user,
    # determine if listing in user watchlist
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        watched_items = user.watched_items.all()
        # determine if listing belongs to current user
        if user == listing_obj.owner:
            user_owned = True

    if bids.count():
        # get bid object with highest amount
        highest_bid = bids.order_by("-amount").first()
        highest_bid_amount = highest_bid.amount
        # set the minimum value for the next future bid
        minimum_bid_amount = highest_bid.amount + decimal.Decimal(0.01)

        # determine if the current user is the current highest bidder
        if highest_bid.bidder == user:
            user_highest_bid = True

    return render(request, "auctions/listing.html", {
        "listing": listing_obj,
        "user_owned": user_owned,
        "bids": bids,
        "comments": comments,
        "category": listing_obj.category,
        "watchedItems": watched_items,
        "minimum_bid": minimum_bid_amount,
        "current_price": highest_bid_amount,
        "user_highest_bid": user_highest_bid
    })


def category_list(request):
    categories = Category.objects.all()
    return render(request, "auctions/category_list.html", {
        "categories": categories
    })


def category_filter(request, name):
    cat_obj = get_object_or_None(Category, name=name)
    if cat_obj is not None:
        return render(request, "auctions/category_results.html", {
            "category": cat_obj,
            "listings": cat_obj.listings.all(),
        })
    return render(request, "auctions/not_found.html", {
        "errMsg": "Category Not Found"
    })


@login_required
def get_watchlist(request, username):
    user = User.objects.get(username=username)
    watched_items = user.watched_items.all()
    return render(request, "auctions/watchlist.html", {
        "listings": watched_items,
        "watchedItems": watched_items
    })


@login_required
def toggle_watchlist_listing(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST["username"])
        try:
            listing = user.watched_items.get(id=request.POST["listing_id"])
        except Listing.DoesNotExist:
            listing = None
        if listing:
            # if listing exists in the user's watched items, remove it
            user.watched_items.remove(listing)
        else:
            # otherwise, add it
            listing = Listing.objects.get(id=request.POST["listing_id"])
            user.watched_items.add(listing)
        HttpResponseRedirect(
            reverse("auctions:listing",
                    kwargs={"listing_id": request.POST["listing_id"]}))
    return HttpResponseRedirect(reverse("auctions:index"))


@ login_required
def new_listing(request):
    if request.method == "POST":
        listing = ListingForm(request.POST)
        if listing.is_valid():
            listing_obj = listing.save(commit=False)
            user = User.objects.get(username=request.user)
            listing_obj.owner = user
            listing_obj.active = True
            listing_obj.save()
            return index(request)
        return HttpResponseRedirect(reverse("auctions:new_listing"))
    # get method for new listing
    form = ListingForm()
    return render(request, "auctions/new_listing.html", {
        "form": form
    })


@ login_required
def close_listing(request):
    if request.method == "POST":
        listing_id = request.POST["listing_id"]
        listing_obj = get_object_or_None(Listing, id=listing_id)
        if listing_obj:
            listing_obj.active = False
            listing_obj.save()
    HttpResponseRedirect(
        reverse("auctions:listing",
                kwargs={"listing_id": request.POST["listing_id"]}))


@ login_required
def bid_on_listing(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST["username"])
        listing_id = request.POST["listing_id"]
        listing_obj = get_object_or_None(Listing, id=listing_id)
        if listing_obj:
            # only allow users who do not own listing to bid
            if user != listing_obj.owner:
                new_bid_price = request.POST["new_bid"]
                bids = listing_obj.listing_bids.all()
                # starting highest bid is just the starting price of listing
                highest_bid = listing_obj.starting_price
                if bids:
                    highest_bid = max(bid.amount for bid in bids)
                # complicated checkpoint: allow the new bid to be created if:
                # there are bids and the new bid is higher than the previous
                # highest bid
                # or there are no bids and the new bid is at least the amount
                # of the starting price
                if ((bids and decimal.Decimal(new_bid_price) > highest_bid) or
                        (not bids and decimal.Decimal(new_bid_price)
                         >= highest_bid)):
                    # create new bid object associated with listing
                    new_bid_obj = Bid(bidder=user,
                                      bid_listing=listing_obj,
                                      amount=new_bid_price)
                    new_bid_obj.save()
                HttpResponseRedirect(
                    reverse("auctions:listing",
                            kwargs={"listing_id": request.POST["listing_id"]}))
    return HttpResponseRedirect(reverse("auctions:index"))


@ login_required
def comment_on_listing(request):
    if request.method == "POST":
        user = User.objects.get(username=request.POST["username"])
        listing_id = request.POST["listing_id"]
        listing_obj = get_object_or_None(Listing, id=listing_id)
        if listing_obj:
            # create new comment associated with listing
            new_comment = request.POST["new_comment"]
            new_comment_obj = Comment(commenter=user,
                                      com_listing=listing_obj,
                                      text=new_comment)
            new_comment_obj.save()
            return HttpResponseRedirect(
                reverse("auctions:listing",
                        kwargs={"listing_id": request.POST["listing_id"]}))
    return HttpResponseRedirect(reverse("auctions:index"))
