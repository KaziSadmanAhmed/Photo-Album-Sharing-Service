from django.db import models


class Comment(models.Model):
    content = models.CharField(max_length=255)
    album = models.ForeignKey("album.Album", related_name="comments", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.content
