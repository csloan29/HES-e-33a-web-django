import os

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import User, Video, Playlist, Comment
from .forms import VideoForm, PlaylistForm


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
        "comments": view_video.video_comments.all(),
        "videos": suggested_videos,
        "playlists": playlists,
        "liked": (user in view_video.likes.all()),
    })


@login_required
def new_video(request):
    if request.method == "POST":
        video_obj = VideoForm(request.POST)
        if video_obj.is_valid():
            video_obj = video_obj.save(commit=False)
            user_obj = User.objects.get(username=request.user)
            video_obj.user = user_obj
            video_obj.save()
            return HttpResponseRedirect(
                reverse("video",
                        kwargs={"video_id": video_obj.id}))
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


@login_required
def new_playlist(request):
    if request.method == "POST":
        playlist_obj = PlaylistForm(request.POST)
        if playlist_obj.is_valid():
            playlist_obj = playlist_obj.save(commit=False)
            user_obj = User.objects.get(username=request.user)
            playlist_obj.user = user_obj
            playlist_obj.save()
            return HttpResponseRedirect(
                reverse("playlist",
                        kwargs={"playlist_id": playlist_obj.id}))
        return HttpResponseRedirect(reverse("new_playlist"))
    # get method for new playlist
    user = User.objects.filter(username=request.user).first()
    playlists = Playlist.objects.filter(user=user)
    form = PlaylistForm()
    return render(request, "the_watch/new-playlist.html", {
        "newPlaylistForm": form,
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


@ login_required
def add_comment(request):
    if request.method == "POST":
        user_obj = User.objects.filter(id=request.POST["user_id"]).first()
        video_obj = Video.objects.filter(id=request.POST["video_id"]).first()
        comment_text = request.POST["comment_text"]
        comment_obj = Comment(
            user=user_obj, text=comment_text, video=video_obj)
        comment_obj.save()
        return HttpResponseRedirect(
            reverse("video",
                    kwargs={"video_id": request.POST["video_id"]}))
    return HttpResponseRedirect(reverse("auctions:index"))


# API Routes
@ login_required
@ csrf_exempt
def toggle_like(request, video_id):
    if request.method == "POST":
        user_obj = User.objects.filter(username=request.user).first()
        video_obj = Video.objects.filter(id=video_id).first()
        if user_obj in video_obj.likes.all():
            video_obj.likes.remove(user_obj)
            status = "Unliked"
        else:
            video_obj.likes.add(user_obj)
            status = "Liked"
        return JsonResponse(
            {
                "message": "toggle like successful",
                "status": status
            }, status=201)
    return JsonResponse(
        {
            "message": "toggle like endpoint only accepts post requests",
        }, status=400)


@login_required
@ csrf_exempt
def add_to_playlist(request, playlist_id, video_id):
    if request.method == "POST":
        playlist_obj = Playlist.objects.filter(id=playlist_id).first()
        video_obj = Video.objects.filter(id=video_id).first()
        # cannot add video to playlist twice
        if video_obj not in playlist_obj.videos.all():
            playlist_obj.videos.add(video_obj)
            print("added video to playlist!")
            return JsonResponse(
                {
                    "message": "Video added successfully to playlist",
                }, status=201)
        return JsonResponse(
            {
                "message": "Video already in playlist",
            }, status=200)
    return JsonResponse(
        {
            "message": "Add to playlist endpoint only accepts post requests",
        }, status=400)
