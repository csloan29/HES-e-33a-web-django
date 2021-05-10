
from django.urls import path

from . import views

urlpatterns = [
    # View Routes
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("account/<int:user_id>", views.account, name="account"),
    path("video/<int:video_id>", views.video, name="video"),
    path("playlist/<int:playlist_id>", views.playlist, name="playlist"),
    path("search/", views.search, name="search"),
    path("new-video", views.new_video, name="new_video"),
    path("new-playlist", views.new_playlist, name="new_playlist"),
    path("add-to-playlist/<int:playlist_id>/<int:video_id>",
         views.add_to_playlist, name="add_to_playlist"),
    path("add-comment", views.add_comment, name="add_comment"),

    # API Routes
    path("toggle-like/<int:video_id>", views.toggle_like, name="toggle_like"),
]
