from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import User, Dog, City
from .forms import DogForm, CityForm


# Create your views here.
def index(request):
    dogs = Dog.objects.all()
    people = User.objects.all()
    cities = City.objects.all()
    return render(request, "dogs/index.html", {
        "dogs": dogs,
        "people": people,
        "cities": cities,
    })


def dog(request, dog_id):
    doggo = Dog.objects.get(pk=dog_id)
    people = doggo.people.all()
    return render(request, "dogs/dog.html", {
        "dog": doggo,
        "people": people
    })


def person(request, username):
    person = User.objects.get(username=username)
    dogs = person.dogs.all()
    return render(request, "dogs/person.html", {
        "person": person,
        "dogs": dogs
    })


def city(request, id):
    city_obj = City.objects.get(id=id)
    dogs = city_obj.residents.all()
    return render(request, "dogs/city.html", {
        "city": city_obj,
        "dogs": dogs
    })


def newdog(request):
    if request.method == "POST":
        doggo = DogForm(request.POST)
        if doggo.is_valid():
            doggo.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = DogForm()
    return render(request, "dogs/newdog.html", {
        "form": form
    })


def newcity(request):
    if request.method == "POST":
        city = CityForm(request.POST)
        if city.is_valid():
            city.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CityForm()
    return render(request, "dogs/newcity.html", {
        "form": form
    })
