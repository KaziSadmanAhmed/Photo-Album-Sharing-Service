from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from .forms import RegisterForm


class CustomLoginView(LoginView):
    template_name = "account/login.html"
    redirect_authenticated_user = True

def register(request):
    if request.user.is_authenticated and request.user.is_active:
        return redirect("album-list")

    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("album-list")
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})
