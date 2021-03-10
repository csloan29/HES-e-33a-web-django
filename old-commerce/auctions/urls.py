from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new-listing", views.register, name="newListing"),
    path("listing/<id>", views.register, name="listing"),
    path("watchlist", views.register, name="watchlist"),
    path("categories", views.register, name="categories"),
    path("admin", views.register, name="admin"),
]