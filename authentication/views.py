from django.shortcuts import render
from requests import Request, post
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils import timezone
from datetime import timedelta
from spotipy import Spotify
from dotenv import load_dotenv
from .utils import *
import os


load_dotenv()


def login(request):
    scopes = "user-top-read user-read-email"

    if not request.session:
        request.session.create()
    url = (
        Request(
            "GET",
            "https://accounts.spotify.com/authorize",
            params={
                "scope": scopes,
                "response_type": "code",
                "redirect_uri": os.getenv("redirect_uri"),
                "client_id": os.getenv("client_id"),
                "client_secret": os.getenv("client_secret"),
            },
        )
        .prepare()
        .url
    )
    return JsonResponse({"redirect_url": url})


def callback(request):
    code = request.GET.get("code")

    response = post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": os.getenv("redirect_uri"),
            "client_id": os.getenv("client_id"),
            "client_secret": os.getenv("client_secret"),
        },
    ).json()

    access_token = response.get("access_token")
    refresh_token = response.get("refresh_token")
    expires_in = 3600
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token
    request.session["expiry"] = (timezone.now() + timedelta(expires_in)).isoformat()

    spotify = Spotify(auth=access_token)
    user_info = spotify.current_user()

    if User.objects.filter(username=user_info["display_name"]):
        user = User.objects.filter(username=user_info["display_name"])[0]
    else:
        user = User.objects.create_user(user_info["display_name"], user_info["email"])
        user.save()

    if user is not None:
        auth_login(request, user)

    return redirect("blu:profile")


def logout(request):
    auth_logout(request)  # this flushes the session too
    del request.session
    return redirect("blu:welcome")
