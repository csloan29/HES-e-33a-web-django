from django.contrib.auth import get_user_model
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
        "2019 Masters Tournament Final Round Broadcast",
        "Watch as Tiger defies all expectations on his march to victory.",
        "https://www.youtube.com/embed/oqYbG8Zhoag",
        "c",
        ["c", "s", "st"]
    ),
    (
        "U.S. Open Epics: Tiger and Rocco",
        "Relive the 2008 U.S. Open at Torrey Pines.",
        "https://www.youtube.com/embed/zodrcuCHh3Q",
        "c",
        ["c", "s", "st"]
    ),
    (
        """STAR WARS THE OLD REPUBLIC Full Movie Cinematic
         4K ULTRA HD All Cinematics Trailers""",
        "All Star Wars the Old Republic cinematic trailers, now in 4k",
        "https://www.youtube.com/embed/DCboJ2GizmM",
        "c",
        ["c", "s", "st"]
    ),
    (
        "Star Wars: The Complete Canon Timeline",
        "This is the entire history of the Star Wars canon as of May 4, 2020",
        "https://www.youtube.com/embed/2TbykYzPxsk",
        "c",
        ["c", "s", "st"]
    ),
    (
        "Longboarding Meets FPV Drones - Norway (4K)",
        "Beautiful drone shots of downhill riders in Norway",
        "https://www.youtube.com/embed/x6S6_6jDv8Q",
        "s",
        ["c", "st"]
    ),
    (
        "Gordon's Quick & Simple Recipes | Gordon Ramsay",
        """While a lot of us are remaining indoors, here are a few quick,
        simple and cheap recipes to follow to learn""",
        "https://www.youtube.com/embed/mhDJNfV7hjk",
        "s",
        ["c", "st"]
    ),
    (
        "GoPro: Best of 2018",
        """2018. The year shaky video died. The year of the longest drift,
         the record rope jump, and the biggest urban downhill ever. """,
        "https://www.youtube.com/embed/KGlv9Lw4QSM",
        "sa",
        ["c", "s", "st"]
    ),
    (
        "GoPro: Best of 2019",
        """Just when we thought smooth couldn't could get any smoother,
         2019 came around""",
        "https://www.youtube.com/embed/SN25SD6Kw2s",
        "sa",
        ["c", "s", "st"]
    ),
    (
        "GoPro: Best of 2020",
        """The Best of 2020. This year had it's challenges, but you
         can't stop this train.""",
        "https://www.youtube.com/embed/Baur2Ypgd60",
        "sa",
        ["c", "s", "st"]
    ),
    (
        "How to Train a Puppy NOT to BITE",
        "Follow these simple steps to help your new pupper not bite",
        "https://www.youtube.com/embed/m9KQegi4r8k",
        "s",
        ["st"]
    ),
    (
        "The Complete Timeline of Middle-earth",
        "The timeline of Middle-earth is truly vast and expansive",
        "https://www.youtube.com/embed/1KroVEOqrBU",
        "st",
        ["c"]
    ),

]

playlists = [
    ("c", "favorites", [
        "Longboarding Meets FPV Drones - Norway (4K)",
        "GoPro: Best of 2020",
        "GoPro: Best of 2019",
        "GoPro: Best of 2018",
    ]),
    ("c", "watch later", [
        "The Complete Timeline of Middle-earth",
        "How to Train a Puppy NOT to BITE",
    ]),
    ("s", "favorites", [
        "GoPro: Best of 2018",
        "GoPro: Best of 2020",
    ]),
    ("s", "motivation", [
        "U.S. Open Epics: Tiger and Rocco",
        "2019 Masters Tournament Final Round Broadcast",
    ]),
    ("sa", "favorites", [
        "U.S. Open Epics: Tiger and Rocco",
        "2019 Masters Tournament Final Round Broadcast",
    ]),
    ("sa", "Star Wars", [
        """STAR WARS THE OLD REPUBLIC Full Movie Cinematic
         4K ULTRA HD All Cinematics Trailers""",
        "Star Wars: The Complete Canon Timeline",
    ]),
    ("st", "favorites", [
        "Star Wars: The Complete Canon Timeline",
    ]),
    ("t", "favorites", []),
]

comments = [
    (
        "c",
        """This is by far the most amazing
         thing ever done in the history of the game.""",
        "2019 Masters Tournament Final Round Broadcast"
    ),
    (
        "s",
        "Tiger is the Goat.",
        "2019 Masters Tournament Final Round Broadcast"
    ),
    (
        "st",
        "They both worked so hard!",
        "U.S. Open Epics: Tiger and Rocco"
    ),
    (
        "c",
        "I love the world Tolkien made!",
        "The Complete Timeline of Middle-earth"
    ),
]

user_model = get_user_model()

# Make Users:
for username, email, password in users:
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.save()

# make Videos:
for title, desc, path, user, likes in videos:
    user_obj = user_model.objects.get(username=user)
    video = Video(
        title=title,
        description=desc,
        path=path,
        user=user_obj
    )
    video.save()

    # add likes to each video
    for user_like in likes:
        user_obj = user_model.objects.get(username=user_like)
        video.likes.add(user_obj)

# add Comments to videos
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
