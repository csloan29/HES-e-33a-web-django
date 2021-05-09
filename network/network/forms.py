from django import forms
from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ""

    class Meta:
        model = Post
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "What's new today?",
                    "rows": 3
                }
            )
        }
