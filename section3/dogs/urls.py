from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dog/<int:dog_id>', views.dog, name="dog"),
    path('person/<str:username>', views.person, name="person"),
    path('city/<int:id>', views.city, name="city"),
    path('newdog', views.newdog, name="newdog"),
    path('newcity', views.newcity, name="newcity")
]
