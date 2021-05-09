from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# meta class to define the 'follower/following'
# relationship between users
class UserFollowing(models.Model):
    user = models.ForeignKey('User',
                             on_delete=models.CASCADE,
                             related_name='following')
    # think 'user above is "following_(this)_user"'
    following_user = models.ForeignKey('User',
                                       on_delete=models.CASCADE,
                                       related_name='followers')
    timestamp = models.DateTimeField(auto_now_add=True)

    # this prevents users from following the same person twice
    class Meta:
        unique_together = ('user', 'following_user')

    def serialize(self):
        return {
            "follower_id": self.user.id,
            "following_id": self.following_user.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }


class Post(models.Model):
    poster = models.ForeignKey('User',
                               on_delete=models.CASCADE,
                               related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    likes = models.ManyToManyField('User',
                                   related_name='posts_liked')

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "poster_id": self.poster.id,
            "likes": [user.id for user in self.likes.all()],
            "text": self.text,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
        }
