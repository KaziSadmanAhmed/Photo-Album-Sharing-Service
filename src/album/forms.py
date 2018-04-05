from django import forms
from django.forms.models import inlineformset_factory

from djangoformsetjs.utils import formset_media_js

from .models import Album, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ("title", "password")
        widgets = {
            "title": forms.TextInput(attrs={"icon": "font"}),
            "password": forms.PasswordInput(attrs={"icon": "lock"})
        }


class PhotoForm(forms.ModelForm):
    title = forms.CharField(required=False)

    class Meta:
        model = Photo
        exclude = ("width", "height")

    class Media(object):
        js = formset_media_js


PhotoFormSet = inlineformset_factory(
    Album,
    Photo,
    form=PhotoForm,
    extra=1
)


class AlbumDetailAuthForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"icon": "lock"}))
