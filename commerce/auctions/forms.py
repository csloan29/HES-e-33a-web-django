from django import forms
from django.forms import ModelForm
from .models import Listing, Category


class ListingForm(ModelForm):
    image_url = forms.URLField(required=False, widget=forms.URLInput(
        attrs={
            "class": "form-control mb-3",
        }
    ))

    category = forms.ModelChoiceField(required=False,
                                      queryset=Category.objects.all(),
                                      widget=forms.Select(
                                          attrs={
                                              "class": "form-control mb-3",
                                          }
                                      ))

    class Meta:
        model = Listing
        fields = ["title", "description",
                  "starting_price", "category", "image_url"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control mb-3"
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control mb-3"
                }
            ),
            "starting_price": forms.NumberInput(
                attrs={
                    "class": "form-control mb-3"
                }
            )
        }
