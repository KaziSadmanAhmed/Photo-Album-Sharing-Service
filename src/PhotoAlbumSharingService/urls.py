from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home.urls"), name="home"),
    path("account/", include("account.urls"), name="account"),
    path("album/", include("album.urls"), name="album"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Only works in debug mode
