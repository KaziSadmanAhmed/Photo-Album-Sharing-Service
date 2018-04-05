from django.contrib import admin
from django.urls import include, path

from .views import AlbumCreateView, AlbumListView, AlbumDetailView, AlbumRatingRedirectView, AlbumCommentRedirectView

urlpatterns = [
    path("add/", AlbumCreateView.as_view(), name="album-create"),
    path("all/", AlbumListView.as_view(), name="album-list"),
    path("<str:uuid>/", AlbumDetailView.as_view(), name="album-detail"),
    path("<str:uuid>/rating", AlbumRatingRedirectView.as_view(), name="album-rating"),
    path("<str:uuid>/comment", AlbumCommentRedirectView.as_view(), name="album-comment")
]
