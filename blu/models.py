from django.db import models
from django.contrib.auth.models import User


class Track(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, to_field="id")
    name = models.CharField(max_length=150)
    artist = models.CharField(max_length=150)
    album = models.CharField(max_length=150)
    image_url = models.CharField(max_length=300, default="")


class Books(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field="id")
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    summary = models.TextField()
    image_url = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField()
