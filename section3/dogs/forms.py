from django.forms import ModelForm
from .models import Dog, City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ["name", "zip_code"]


class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = ["name", "age", "home", "people", "photo"]
