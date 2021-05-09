from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    path = models.CharField(max_length=60)
    datetime = models.DateTimeField(
        auto_now=True, blank=False, null=False)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_videos")
    likes = models.ManyToManyField("User", related_name="videos_liked")


class Playlist(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    videos = models.ManyToManyField("Video", related_name="included_lists")


class Comment(models.Model):
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="user_comments")
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="video_comments")
