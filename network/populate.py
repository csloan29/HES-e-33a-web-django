from django.contrib.auth import get_user_model
from network.models import User, UserFollowing, Post

users = [
    ("c", "c@c.com", "c"),  # many
    ("s", "s@s.com", "s"),  # many
    ("t", "t@t.com", "t"),  # one
    ("k", "k@k.com", "k"),  # many
    ("r", "r@r.com", "r"),  # none
]

followings = [
    ("c", "s"),
    ("c", "t"),
    ("c", "k"),
    ("s", "c"),
    ("t", "s"),
    ("k", "c"),
    ("k", "s"),
]

posts = [
    (
        "c",
        """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Scelerisque mauris pellentesque pulvinar pellentesque habitant morbi
        tristique senectus. Velit aliquet sagittis id consectetur purus ut.""",
        ["s", "t"]
    ),
    (
        "c",
        """Et magnis dis parturient montes nascetur ridiculus mus
        mauris vitae. Non curabitur gravida arcu ac. Odio aenean sed adipiscing
        diam donec adipiscing tristique. Ultrices eros in cursus turpis massa.
        Tortor at risus viverra adipiscing at in tellus integer feugiat.
        Sit amet consectetur adipiscing elit.""",
        ["k", "t"]
    ),
    (
        "s",
        """Semper feugiat nibh sed pulvinar proin. Iaculis urna id
        volutpat lacus laoreet non curabitur. Hac habitasse platea
        dictumst vestibulum. Vestibulum lorem sed risus ultricies tristique
        nulla aliquet enim tortor. Posuere sollicitudin aliquam ultrices
        sagittis orci a scelerisque purus semper.""",
        ["s"]
    ),
    (
        "t",
        """Aenean sed adipiscing diam donec adipiscing tristique risus
        nec feugiat. Facilisi etiam dignissim diam quis enim lobortis.
        Vel pretium lectus quam id leo in vitae turpis. Maecenas ultricies
        mi eget mauris pharetra et ultrices neque. Accumsan sit amet nulla
        facilisi morbi tempus iaculis urna. Aenean vel elit scelerisque
        mauris pellentesque pulvinar.""",
        ["c"]
    ),
    (
        "k",
        """Sed risus ultricies tristique nulla aliquet enim tortor at.
        Ut aliquam purus sit amet luctus venenatis lectus magna.
        Nisi porta lorem mollis aliquam ut porttitor leo a diam.
        Eu ultrices vitae auctor eu augue. Sed libero enim sed faucibus turpis.
        Vitae suscipit tellus mauris a diam maecenas.""",
        []
    ),
    (
        "k",
        """Faucibus purus in massa tempor nec feugiat. Lectus urna duis
        convallis convallis tellus. Massa placerat duis ultricies lacus.
        At risus viverra adipiscing at in tellus. Pellentesque elit eget
        gravida cum sociis natoque penatibus. Nullam non nisi est sit amet.""",
        []
    ),
    (
        "k",
        """Sodales ut eu sem integer vitae.""",
        ["c", "s", "t"]
    ),
    (
        "k",
        """Elementum tempus egestas sed sed risus.
        Velit ut tortor pretium viverra suspendisse potenti nullam ac. Volutpat
        sed cras ornare arcu. Lacus laoreet non curabitur gravida arcu.
        Vulputate dignissim suspendisse in est ante in nibh mauris cursus.
        Quis lectus nulla at volutpat diam ut venenatis. At quis risus sed
        vulputate odio ut enim blandit volutpat. Curabitur gravida arcu ac
        tortor dignissim. Fusce ut placerat orci nulla. Euismod quis viverra
        nibh cras pulvinar mattis. Iaculis eu non diam phasellus vestibulum
        lorem. Nisl nisi scelerisque eu ultrices vitae auctor eu. Faucibus
        interdum posuere lorem ipsum. Scelerisque mauris pellentesque pulvinar
        pellentesque habitant morbi tristique. Tellus at urna condimentum
        mattis pellentesque. Ultricies integer quis auctor elit.
        Consectetur adipiscing elit duis tristique sollicitudin nibh sit
        amet commodo. Eget duis at tellus at urna condimentum mattis.""",
        ["c", "s", "t"]
    ),
]

# Make Users:
for username, email, password in users:
    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.save()

# make Posts:
for user, text, likes in posts:
    user_model = get_user_model()
    user = user_model.objects.get(username=user)
    post = Post(
        poster=user,
        text=text
    )
    post.save()

    # add likes to each post
    for like in likes:
        like_user = user_model.objects.get(username=like)
        post.likes.add(like_user)

# generate followings
for follower, followed in followings:
    user_model = get_user_model()
    userFollower = user_model.objects.get(username=follower)
    userFollowed = user_model.objects.get(username=followed)
    following_obj = UserFollowing(user=userFollower,
                                  following_user=userFollowed)
    following_obj.save()

# COMMANDS FOR RUNNING POPULATE IN SHELL
# p3m shell
# exec(open('populate.py').read())
