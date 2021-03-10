from django.contrib.auth import get_user_model
from auctions.models import User, Listing, Bid, Comment, Category
from image_addresses import (LIGHTSABER, SABACC, FETT_ARMOR,
                             PENDANT, PODRACER, DICE, ROBES,
                             DROIDEKA, SHIP)


category_types = [
    ("Keepsake"),
    ("Weapon"),
    ("Competition"),
    ("Utility")
]

users = [
    ("Luke", "luke@theforce.com", "l"),
    ("Han", "han@quikshot.com", "h"),
    ("Din", "din@theway.com", "d"),
    ("Anakin", "anakin@mustafar.com", "a"),
    ("Cobb", "cobb@outskirts.com", "c"),
    ("Lea", "lea@alderaan.org", "l"),
]

listings = [
    ("Skywalker Lightsaber", 199.99, "It's Ani's... NOT Rey's.",
     "Luke", LIGHTSABER, "Weapon"),
    ("Sabacc Game", 16.99, "The game Lando's only lost once at",
     "Han", SABACC, "Competition"),
    ("Boba Fett's Armor", 1000.00, "Just hope Boba's still in the pit...",
     "Din", FETT_ARMOR, "Weapon"),
    ("Princess Amidala's Pendant", 85.00,
     "Unfortunately does NOT help with repelling sand.",
     "Anakin", PENDANT, "Keepsake"),
    ("Little Ani's Podracer", 5000.00, "Well...Most of it..",
     "Cobb", PODRACER, "Keepsake"),
    ("Han Solo's Dice", 65.00, "Never tell me the odds..!",
     "Lea", DICE, "Keepsake"),
    ("Jedi Tunic and Robes", 150.00,
     "I REALLY don't need these anymore..",
     "Anakin", ROBES, "Utility"),
    ("Droideka", 2000.00, "Very fast, veeery dangerous",
     "Cobb", DROIDEKA, "Weapon"),
    ("Obi-Wan's Ship", 65.00,
     "Not even sure how I happen to have this hunk of junk..",
     "Din", SHIP, "Keepsake"),
]

watchlists = [
    ("Luke", "Sabacc Game"),
    ("Luke", "Little Ani's Podracer"),
    ("Lea", "Boba Fett's Armor"),
    ("Lea", "Princess Amidala's Pendant"),
    ("Din", "Skywalker Lightsaber"),
    ("Din", "Han Solo's Dice"),
    ("Anakin", "Sabacc Game"),
    ("Cobb", "Sabacc Game"),
    ("Han", "Sabacc Game"),
]

bids = [
    ("Sabacc Game", "Luke", 19.00),
    ("Sabacc Game", "Han", 21.00),
    ("Princess Amidala's Pendant", "Lea", 90.00),
    ("Skywalker Lightsaber", "Cobb", 210.00),
    ("Boba Fett's Armor", "Cobb", 1010.00),
]

comments = [
    ("Sabacc Game", "Han",
     "I think I know a guy who needs a little practice at this..."),
    ("Sabacc Game", "Lea", "Don't start this again, Han!"),
    ("Skywalker Lightsaber", "Cobb", "I need this... bad"),
    ("Skywalker Lightsaber", "Anakin",
     "Cobb, Your lack of patience is... disturbing."),
    ("Princess Amidala's Pendant", "Lea",
     "A little overpriced... but it goes great with white."),
]

# Make Users:
for username, email, password in users:
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.save()

# Make Categories:
for cat_type in category_types:
    cat = Category(name=cat_type)
    cat.save()

# make Listings associated with Users (active is default to true):
for title, price, description, owner, image, category in listings:
    user_model = get_user_model()
    user = user_model.objects.get(username=owner)
    category_obj = Category.objects.get(name=category)
    listing = Listing(title=title, starting_price=price,
                      description=description, owner=user,
                      image_url=image, category=category_obj)
    listing.save()

# make watchlists
for user, listing in watchlists:
    user_model = get_user_model()
    user = user_model.objects.get(username=user)
    listing_obj = Listing.objects.get(title=listing)
    user.watched_items.add(listing_obj)

# make bids and associate them with the correct listing
for listing, bidder, bid in bids:
    user_model = get_user_model()
    user = user_model.objects.get(username=bidder)
    listing = Listing.objects.get(title=listing)
    bid = Bid(bidder=user, amount=bid, bid_listing=listing)
    bid.save()

# make comments and associate them with the correct listing
for listing, commenter, text in comments:
    user_model = get_user_model()
    user = user_model.objects.get(username=commenter)
    listing = Listing.objects.get(title=listing)
    comment = Comment(commenter=user, text=text, com_listing=listing)
    comment.save()
