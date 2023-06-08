from rest_framework import serializers
from .models import *


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        exclude = ["user"]


class BookSerlaizer(serializers.ModelSerializer):
    class Meta:
        model= Books
        exclude = ["id"]
