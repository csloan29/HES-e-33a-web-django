import os
from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import User, Video, Playlist, Comment
from .forms import VideoForm


def index(request):
    playlists = []
    videos = []
    user = User.objects.filter(username=request.user).first()
    if user is not None:
        playlists = Playlist.objects.filter(user=user)
        videos = Video.objects.filter(~Q(user=user))
    else:
        videos = Video.objects.all()
    return render(request, "the_watch/index.html", {
        "videos": videos,
        "playlists": playlists
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
            return render(request, "the_watch/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "the_watch/login.html")


@login_required
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
            return render(request, "the_watch/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "the_watch/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "the_watch/register.html")


@login_required
def account(request, user_id):
    user = User.objects.filter(id=user_id).first()
    playlists = Playlist.objects.filter(user=user)
    videos = Video.objects.filter(user=user)
    return render(request, "the_watch/account.html", {
        "profile_user": user,
        "videos": videos,
        "video_count": len(videos),
        "playlists": playlists,
    })


def video(request, video_id):
    view_video = Video.objects.filter(id=video_id).first()
    suggested_videos = Video.objects.all()
    playlists = []
    user = User.objects.filter(username=request.user).first()
    if user is not None:
        playlists = Playlist.objects.filter(user=user)
    return render(request, "the_watch/video.html", {
        "video": view_video,
        "videos": suggested_videos,
        "playlists": playlists
    })


@login_required
def new_video(request):
    if request.method == "POST":
        video_obj = VideoForm(request.POST)
        if video_obj.is_valid():
            video_obj = video_obj.save(commit=False)
            user = User.objects.get(username=request.user)
            video_obj.owner = user
            video_obj.save()
            return index(request)
        return HttpResponseRedirect(reverse("new_video"))
    # get method for new video
    user = User.objects.filter(username=request.user).first()
    playlists = Playlist.objects.filter(user=user)
    form = VideoForm()
    return render(request, "the_watch/new-video.html", {
        "newVideoForm": form,
        "playlists": playlists,
    })


@login_required
def playlist(request, playlist_id):
    user = User.objects.filter(username=request.user).first()
    playlists = Playlist.objects.filter(user=user)
    playlist_obj = Playlist.objects.filter(id=playlist_id).first()
    return render(request, "the_watch/playlist.html", {
        "playlist": playlist_obj,
        "videos": playlist_obj.videos.all(),
        "playlists": playlists,
    })


def search(request):
    if request.method == "POST":
        query = request.POST["query"]
        videos = Video.objects.filter(title__contains=query)
        users = User.objects.filter(username__contains=query)
        playlists = []
        user = User.objects.filter(username=request.user).first()
        if user is not None:
            playlists = Playlist.objects.filter(user=user)
        return render(request, "the_watch/search.html", {
            "videos": videos,
            "users": users,
            "playlists": playlists,
        })
    return render(request, "the_watch/search.html", {
        "video_results": Video.objects.all(),
        "user_results": [],
        "playlists": [],
    })


# API Routes
@login_required
def toggle_like(request):
    pass


@login_required
def add_comment(request):
    pass


def get_video_from_storage(file_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath("__file__")))
    file = FileWrapper(open(base_dir+'/'+file_name, 'rb'))
    return file
