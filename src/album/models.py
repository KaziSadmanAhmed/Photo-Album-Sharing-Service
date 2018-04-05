from django.db import models
from django.conf import settings


# Album model
class Album(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="albums", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    uuid = models.CharField(max_length=32) # For generating unique random url
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    ratings = models.PositiveIntegerField() # Total sum of ratings
    raters = models.PositiveIntegerField() # Total number of raters

    class Meta:
        ordering = ("-id",)

    def get_rating(self):
        try:
            return round(self.ratings / self.raters)
        except Exception:
            return 0

    def __str__(self):
        return self.title if self.title else "Unnamed"


# Photo model
class Photo(models.Model):
    title = models.CharField(max_length=255)
    width = models.PositiveIntegerField(default=0)
    height = models.PositiveIntegerField(default=0)
    image = models.ImageField(null=False, blank=False, width_field="width", height_field="height")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    album = models.ForeignKey(Album, related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.title if self.title else "Unnamed"
