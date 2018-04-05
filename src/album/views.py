from uuid import uuid4

from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Album
from .forms import AlbumForm, PhotoFormSet, AlbumDetailAuthForm
from comment.forms import CommentForm


# Create Album View
class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = "album/create.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["photo_formset"] = PhotoFormSet(self.request.POST, self.request.FILES)
        else:
            data["photo_formset"] = PhotoFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        photo_formset = context["photo_formset"]

        if form.is_valid() and photo_formset.is_valid():
            album = form.save(commit=False)
            album.user = self.request.user
            album.password = make_password(form.cleaned_data["password"])
            album.uuid = uuid4().hex
            album.save()

            photos = photo_formset.save(commit=False)
            for photo in photos:
                photo.album = album
                photo.save()

        else:
            return render(self.request, template_name=self.template_name, context=self.get_context_data())

        return super().form_valid(form)


# List Albums View
class AlbumListView(LoginRequiredMixin, ListView):
    context_object_name = "albums"
    template_name = "album/list.html"
    login_url = "login"

    def get_queryset(self):
        queryset = Album.objects.filter(user=self.request.user)
        return queryset


# Specific Album View
class AlbumDetailView(View):
    template_name = "album/detail.html"
    auth_template_name = "album/detail_auth.html"

    def get(self, request, *args, **kwargs):
        album = get_object_or_404(Album, uuid=kwargs.get("uuid"))
        if request.user.is_authenticated and request.user.is_active:
            if album.user == request.user:
                return render(request, template_name=self.template_name, context={"album": album, "uuid": kwargs.get("uuid"), "comment_form": CommentForm()}) # Album publisher
        return render(request, template_name=self.auth_template_name, context={"auth_form": AlbumDetailAuthForm(), "uuid": kwargs.get("uuid")}) # Unauthorized user

    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, uuid=kwargs.get("uuid"))
        auth_form = AlbumDetailAuthForm(request.POST)
        if auth_form.is_valid():
            if check_password(auth_form.cleaned_data["password"], album.password):
                return render(request, template_name=self.template_name, context={"album": album, "uuid": kwargs.get("uuid"), "comment_form": CommentForm()})
        auth_form.add_error("password", "Error")
        return render(request, template_name=self.auth_template_name, context={"auth_form": auth_form, "uuid": kwargs.get("uuid")})


class AlbumRatingRedirectView(RedirectView):
    permanent = False
    pattern_name = "album-detail"

    def get_redirect_url(self, *args, **kwargs):
        if self.request.POST.get("rating") and 1 < int(self.request.POST.get("rating")) <= 5:
            album = get_object_or_404(Album, uuid=kwargs.get("uuid"))
            album.ratings += int(self.request.POST.get("rating"))
            album.raters += 1
            album.save()
        return super().get_redirect_url(*args, **kwargs)


class AlbumCommentRedirectView(RedirectView):
    permanent = False
    pattern_name = "album-detail"

    def post(self, request, *args, **kwargs):
        album = get_object_or_404(Album, uuid=kwargs.get("uuid"))
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.album = album
            comment.save()
        return self.get(request, *args, **kwargs)
