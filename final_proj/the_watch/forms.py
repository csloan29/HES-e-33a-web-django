from django import forms
from django.forms import ModelForm
from .models import Video


class VideoForm(ModelForm):
    path = forms.URLField(required=True,
                          label="YouTube URL",
                          widget=forms.URLInput(
                              attrs={
                                  "class": "form-control mb-3",
                                  "placeholder": "Please add YouTube embed URL"
                              }
                          ))

    class Meta:
        model = Video
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control mb-3"
                }
            )
        }
