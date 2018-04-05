from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, help_text="Required. First name.")
    last_name = forms.CharField(max_length=30, help_text="Required. Last name.")
    email = forms.EmailField(max_length=255, help_text="Required. Valid email addressself.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2",)
