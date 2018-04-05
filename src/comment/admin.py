from django.contrib import admin

from .models import Comment


# Photo Model Stacked Inline Admin
class CommentInlineAdmin(admin.StackedInline):
    model = Comment
    extra = 1
    fields = ("content",)


admin.site.register(Comment)
