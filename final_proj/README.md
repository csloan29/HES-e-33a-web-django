# CSCI E-33a Final Project - "The Watch"

The Watch is a YouTube clone. It allows users to:
* Create a profile
* upload video embed links from YouTube and see other users' videos
* Watch uploaded videos
* Like and unlike videos
* Comment on videos
* Create new playlists
* Add videos to playlists

# Installation and usage

There are no additional python packages required to run this project.
All additional JavaScript and CSS libraries were already included in the main HTML page.

To start The Watch application, simply run:

```bash
    python manage.py runserver
```

Additional Demo Data should already be included in the uploaded zip files (I did not remove the sqlite.db file). However, if for whatever reason the db file does not work or is not there, You may add demo data to the application for testing by running:

```bash
    python manage.py shell
    >>> exec(open("populate.py").read())
```

This demo data will give you access to 5 different users (they're my family members, that's why they are named as such, haha).
* C
  * username: c
  * password: c
* S
  * username: s
  * password: s
* Sa
  * username: sa
  * password: sa
* St
  * username: st
  * password: st
* T
  * username: t
  * password: t

The users C, S, and Sa all have multiple entries of data, from multiple likes, multiple videos, and multiple playlists. The user St is my single data user, who has only one video, one like etc. Finally, the user T is my no data user, and has no videos, likes etc.

# Files

## -- Templates --

#### layout.html
This was one of the most involved views in the app. It contains the code for not only the top nav bar, but also the side nav bar, as well. Most of the design decisions I made because I was trying to imitate YouTube as best I could. Therefore, I decided to put playlist access in this side bar as well as other features like the home button, while the search ability and account access remained in the top navigation bar.

#### index.html
The main index page is a very simple display which shows a card view display of all the currently uploaded videos. This view does not include a user's uploaded videos, if a user is logged in. I wanted this to behave more like a feed than an 'all videos' feature.
<br>
The view is composed of an inherited template, which gives the index view access to the list of video cards. This is the only place this template is used. I was initially planning on using multiple card views on the main page to display different video lists for the user feed, but due to time constraints, this did not happen.
<br>
Since I decided to show the videos as a card display, I also didn't feel the need to allow the user to browse the videos in reverse chronological order. It felt more like a browsing activity and less of a need to see chronology.

#### login.html & register.html
These views simply allow a user to either login or register for the first time.

#### account.html
This view allows a user to view their account, the number of videos they have uploaded, and also a list of all the videos they have uploaded. They can also click a button to add a new video from here.

#### new-video.html
This view simply allows a user to upload a new video. It's accessed either from the user's account page or the account main menu in the navbar in the upper right corner

#### playlist.html
This view allows a user to view their playlist of videos.

#### new-playlist.html
This view simply allows a user to upload a new playlist. Once the playlist is created, the user then visits the playlist.

#### search.html
This view is the result of querying the video and user database for matches containing the string supplied to the search bar. Therefore, if there are any video titles or user usernames containing this string, they will be shown here.

#### video.html
This view is the most involved view of the app. I wanted this main page to feel almost exactly like the YouTube main video viewing page, and so all design decisions reflect that goal. I accessed the iframe functionality to allow users access to the video controls as well as fullscreen capability.



## --- Static Files ---

#### styles.css
This file simply holds some of the custom styling needed for the app, especially for the side navigation bar, which was not supported by default by Bootstrap.

#### index.js
This file contains the JavaScript necessary to toggle the side nav open and closed, as well as toggle the video like button asynchronously without reload.

This is also where I control the add to playlist feature, which also displays an alert that details whether the video was added to the playlist or not (not added only when the video is already in the playlist).

#### assets/
This folder simply contains the icon and png images used as the main logo

## --- Python Files ---

#### urls.py
This file is simple enough. It only contains a list of the available URLs. Only one endpoint is singled out as being an API endpoint and not an endpoint which produces a View.

#### forms.py
This file contains the forms necessary for adding data. There are no notable design decision here, apart from needing to include special bootstrap classes for styling purposes.

#### models.py
This file contains the models for the django db. I decided to create 4 models, a User, a Video object, a Playlist object, and a Comment object.

#### views.py
This is definitely the most complex of the python files created. Most of the design decisions in this file are also pretty standard, however some notable ones stand out.
<br>
I decided to create both a video route as well as a new video route, since the new video functionality would have both a create a new video and needed to fetch the new video view, where the new video form would be located.
<br>
On several view functions, I required the user to be logged in, like the playlist view and the new video view. I did not require it on others, however, most notable the account view, since a user that was not logged in could still view the accounts of other users.
<br>

#### populate.py
This file can be run within the python shell to populate the Django DB before use.

# What I did NOT accomplish

There were several things I wanted to accomplish in this project, but was unable to due to time constraints. The biggest hang-up I encountered was trying to configure Django the right way so as to store and then retrieve media files, like the videos for this app.
<br><br>
I unfortunately was not able to figure out this functionality in time, and so I had to pivot and make it so that users simply had to upload a YouTube embed link in order to add their video to the app. This allowed me to avoid having to manage the media files of the app altogether and simply store the YouTube link as a CharField.

I also decided not to include the category tag functionality to the UI. I felt that this functionality was a clunky and cumbersome to the user and that in a better app this "category" feature would be handled all on the backend through natural language processing.

Lastly, There were several other features I wanted to add to this app, but again due to time constraints I was not able to finish them.
