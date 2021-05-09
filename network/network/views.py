import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Prefetch

from .models import User, UserFollowing, Post
from .forms import PostForm


def index(request):
    return HttpResponseRedirect(reverse("posts", kwargs={"page": 1}))


def posts(request, page):
    if request.method == "POST":
        post = PostForm(request.POST)
        if post.is_valid():
            # create new post from form data
            post_obj = post.save(commit=False)
            user = User.objects.get(username=request.user)
            post_obj.poster = user
            post_obj.save()
        context_path = request.POST["context_path"]
        return HttpResponseRedirect(context_path)
    else:
        # fetch posts
        posts = Post.objects.all()
        if posts:
            # order posts by most recent
            posts = posts.order_by("-timestamp").all()
        else:
            # send empty list instead of None for no posts
            posts = []
        # paginate results
        paginator = Paginator(posts, 10)
        return render(request, "network/index.html", {
            "new_post_form": PostForm(),
            "posts": [post.serialize() for post in paginator.page(page)],
            "page_num": page,
            "page_count": paginator.num_pages,
            "page_range": range(1, paginator.num_pages + 1)
        })


@login_required
def following(request, page):
    user = User.objects.get(username=request.user)
    relationships = user.following.all()
    posts = None
    # for each following relationship, fetch posts and concatenate
    # in one queryset
    for r in relationships:
        if posts is None:
            posts = r.following_user.posts.all()
        else:
            # concatenate prior query sets with found queryset
            posts = posts | r.following_user.posts.all()
    if posts:
        # order by most recent
        posts = posts.order_by("-timestamp").all()
    else:
        # send empty list instead of None for no posts
        posts = []
    # paginate results
    paginator = Paginator(posts, 10)
    return render(request, "network/following.html", {
        "posts": [post.serialize() for post in paginator.page(page)],
        "page_num": page,
        "page_count": paginator.num_pages,
        "page_range": range(1, paginator.num_pages + 1)
    })


@login_required
def profile(request, username, page):
    # get user object
    user = User.objects.get(username=request.user)
    # get profile user object
    profile_user = User.objects.get(username=username)
    # get posts of profile user
    posts = profile_user.posts.all()
    if posts:
        # order posts by most recent
        posts = posts.order_by("-timestamp").all()
    else:
        # send empty list instead of None for no posts
        posts = []
    # paginate results
    paginator = Paginator(posts, 10)
    return render(request, "network/profile.html",
                  {
                      "profile_id": profile_user.id,
                      "username": username,
                      "follower_count": len(profile_user.followers.all()),
                      "follow_count": len(profile_user.following.all()),
                      "post_count": len(profile_user.posts.all()),
                      "posts": [
                          post.serialize() for post in paginator.page(page)
                      ],
                      "page_num": page,
                      "page_count": paginator.num_pages,
                      "page_range": range(1, paginator.num_pages + 1),
                      "user_followed_user_ids": [
                          userFollowing.following_user.id
                          for userFollowing in user.following.all()
                      ],
                      "new_post_form": PostForm(),
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
@csrf_exempt
def post_edit(request, post_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        post_obj = Post.objects.get(id=post_id)
        # prevent user from editing other user"s posts
        if (user.id != post_obj.poster.id):
            return JsonResponse({
                "error": "Cannot edit another user's posts"
            }, status=400)

        data = json.loads(request.body)
        post_obj.text = data["text"]
        post_obj.save()
        return JsonResponse(
            {
                "message": f"post edit with id {post_id} successful.",
                "post": post_obj.serialize()
            }, status=201)


@login_required
@csrf_exempt
def toggle_like(request, post_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        post = Post.objects.get(id=post_id)
        if user in post.likes.all():
            post.likes.remove(user)
            status = "unliked"
        else:
            post.likes.add(user)
            status = "liked"
        return JsonResponse(
            {
                "message": "toggle like successful.",
                "status": status,
                "likes": len(post.likes.all())
            }, status=201)


@login_required
@csrf_exempt
def toggle_follow(request, user_id):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        following_user = User.objects.get(id=user_id)
        # prevent user from following themselves
        if (user.id == following_user.id):
            return JsonResponse({
                "error": "Follow of one's self not allowed."
            }, status=400)

        following_ids = [
            following.following_user.id
            for following in user.following.all()]
        if user_id in following_ids:
            user.following.get(following_user__id=user_id).delete()
            status = "unfollowed"
        else:
            userFollowing = UserFollowing(
                user=user, following_user=following_user)
            userFollowing.save()
            status = "followed"
        return JsonResponse(
            {
                "message": "toggle follow successful",
                "status": status
            }, status=201)
