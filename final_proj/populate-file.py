import os

from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from django.core.files import File

from the_watch.models import User, Video, Playlist, Comment

users = [
    ("c", "c@c.com", "c"),      # many
    ("s", "s@s.com", "s"),      # many
    ("sa", "sa@sa.com", "sa"),  # many
    ("st", "st@st.com", "st"),  # one
    ("t", "t@t.com", "t"),      # none
]

videos = [
    (
        "Bloodborne - The Great Jump Scare!",
        "one of the great jump scares from a great game!",
        "Bloodborne.mp4",
        "c",
        ["c", "s", "st"]
    ),
    (
        """Dark Souls III NOPE""",
        "All Star Wars the Old Republic cinematic trailers, now in 4k",
        "Dark_souls_nope.mp4",
        "c",
        ["c", "s", "st"]
    ),
    (
        "Dark Souls Nope AGAIN",
        "I absolutely do not want to go through with this...",
        "Dark_Souls.mp4",
        "c",
        ["c", "s", "st"]
    ),
    (
        "Bryson DeChambeau Hole in 1!",
        "An amazing hole in 1 by one of the best on tour",
        "DeChambeau.mp4",
        "sa",
        ["c", "s", "st"]
    ),
    (
        "Nicklaus Jr. with a great hole in 1!",
        "An amazing hole in 1. It must be in the genes",
        "Nicklaus_jr_holein1.mp4",
        "sa",
        ["c", "s", "st"]
    ),
    (
        "Nicklaus Showing us all just how easy it is",
        "This man is on an entirely other level...!",
        "Nicklaus_putt.mp4",
        "sa",
        ["c", "s", "st"]
    ),
    # (
    #     "GoPro best of 2020",
    #     "2020 wasn't ALL bad",
    #     "Nicklaus_putt.mp4",
    #     "s",
    #     ["c", "st"]
    # ),
    # (
    #     "GoPro Awards: Million Dollar Challenge",
    #     """A snapshot of all the amazing million dollar videos""",
    #     "Nicklaus_putt.mp4",
    #     "s",
    #     ["c", "st"]
    # ),
    # (
    #     "GoPro: Hero Max 8",
    #     "A Sneak Peak at what the Hero Max 8 is capable of",
    #     "Nicklaus_putt.mp4",
    #     "s",
    #     ["st"]
    # ),
    (
        "White Phosphorus is Terrifying",
        """White Phosphorus is stored under water to protect it
         from air and it starts smoking phosphorus
         oxides the moment it's exposed.""",
        "White_phosphorus.mp4",
        "st",
        ["c"]
    ),

]

playlists = [
    ("c", "favorites", [
        "Bryson DeChambeau Hole in 1!",
    ]),
    ("c", "watch later", [
        "Nicklaus Jr. with a great hole in 1!",
    ]),
    ("s", "favorites", [
        "Bryson DeChambeau Hole in 1!",
    ]),
    ("s", "motivation", [
        "Nicklaus Jr. with a great hole in 1!",
    ]),
    ("sa", "favorites", [
        "Bloodborne - The Great Jump Scare!",
    ]),
    ("st", "favorites", [
        "Bloodborne - The Great Jump Scare!",
    ]),
    ("t", "favorites", []),
]

comments = [
    (
        "c",
        """Man, he just walked up to it, too!""",
        "Nicklaus Showing us all just how easy it is"
    ),
    (
        "s",
        "Seriously amazing.",
        "Nicklaus Showing us all just how easy it is"
    ),
    (
        "st",
        "I can't believe he did that!",
        "Nicklaus Showing us all just how easy it is"
    ),
    (
        "c",
        "Yeesh, that stuff is crazy",
        "White Phosphorus is Terrifying"
    ),
]

user_model = get_user_model()

# Make Users:
for username, email, password in users:
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.save()

# make Videos:
for title, desc, video, user, likes in videos:
    user_obj = user_model.objects.get(username=user)

    file = open(video, "r", encoding="latin1")
    video_file = File(file)

    video = Video(
        title=title,
        description=desc,
        file=video_file,
        user=user_obj
    )
    video.save()

    # add likes to each video
    for user_like in likes:
        user_obj = user_model.objects.get(username=user_like)
        video.likes.add(user_obj)

    file.close()

# add comments to videos
for user, text, video_title in comments:
    user_obj = user_model.objects.get(username=user)
    video_obj = Video.objects.get(title=video_title)
    comment = Comment(
        text=text,
        user=user_obj,
        video=video_obj
    )
    comment.save()


# generate playlists
for user, title, videos in playlists:
    user_obj = user_model.objects.get(username=user)
    playlist = Playlist(
        title=title,
        user=user_obj,
    )
    playlist.save()

    # add videos to playlist
    for video_title in videos:
        video_obj = Video.objects.get(title=video_title)
        playlist.videos.add(video_obj)

# COMMANDS FOR RUNNING POPULATE IN SHELL
# p3m shell
# exec(open("populate.py").read())
