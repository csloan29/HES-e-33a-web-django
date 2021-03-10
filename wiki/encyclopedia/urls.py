from django.urls import path

from . import views

app_name = 'enc'
urlpatterns = [
    path("", views.renderIndex, name="index"),
    path("new", views.addNewEntry, name="new"),
    path("wiki/<str:title>/edit", views.editEntry, name="edit"),
    path("wiki/<str:title>", views.getEntry, name="wiki"),
    path("search", views.doSearch, name="search"),
    path("random", views.getRandom, name="random"),
    path("404", views.errNotFound, name="404"),
]
