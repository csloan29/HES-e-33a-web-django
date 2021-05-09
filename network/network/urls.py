from django.urls import path

from . import views

urlpatterns = [
    # UI & API hybrid routes
    path("", views.index, name="index"),
    path("posts/<int:page>", views.posts, name="posts"),
    path("following/<int:page>", views.following, name="following"),
    path("profile/<str:username>/<int:page>", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routes
    path("post-edit/<int:post_id>", views.post_edit, name="post_edit"),
    path("toggle-like/<int:post_id>",
         views.toggle_like, name="toggle_like"),
    path("toggle-follow/<int:user_id>",
         views.toggle_follow, name="toggle_follow"),
]
