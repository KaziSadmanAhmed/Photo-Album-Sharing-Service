from django.contrib import admin

from .models import Album, Photo
from comment.admin import CommentInlineAdmin


# Photo Model Stacked Inline Admin
class PhotoInlineAdmin(admin.StackedInline):
    model = Photo
    extra = 1
    readonly_fields = ("width", "height") # To disable the width and height fields


# Album Model Admin
class AlbumAdmin(admin.ModelAdmin):
    inlines = (PhotoInlineAdmin, CommentInlineAdmin)


# Photo Model Admin
class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ("width", "height") # To disable the width and height fields

    class Meta:
        model = Photo


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
