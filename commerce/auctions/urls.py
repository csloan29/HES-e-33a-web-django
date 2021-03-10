from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("watchlist/<str:username>", views.get_watchlist, name="watchlist"),
    path("toggle_watchlist", views.toggle_watchlist_listing,
         name="toggle_watchlist"),
    path("categories", views.category_list, name="categories"),
    path("category/<str:name>",
         views.category_filter, name="category"),
    path("listing/<int:listing_id>", views.get_listing, name="listing"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("comment_on_listing",
         views.comment_on_listing, name="comment_on_listing"),
    path("bid_on_listing", views.bid_on_listing, name="bid_on_listing"),
]
