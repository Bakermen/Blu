from django.shortcuts import render
from django.db import connection
from .serializers import *
from authentication.utils import refresh_token
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.conf import settings
from spotipy import Spotify
from requests import get
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from numpy.linalg import norm
from spotipy import Spotify
from .models import *
from .utils import *
import os
import json
import tensorflow as tf
import pandas as pd
import numpy as np
import joblib
import itertools
import csv


# view functions
@login_required()
def user_info(request):
    spotify = Spotify(auth=request.session["access_token"])
    response = spotify.current_user()
    try:
        username = response["display_name"]
        email = response["email"]
        spotify_url = response["external_urls"]["spotify"]
        followers = response["followers"]["total"]
        image_url = response["images"][0]["url"]
    except:
        username = response["display_name"]
        email = response["email"]
        spotify_url = response["external_urls"]["spotify"]
        followers = response["followers"]["total"]
        image_url = "static/default_image.svg"
    context = {
        "active_tab": "profile",
        "user_info": {
            "username": username,
            "email": email,
            "followers": followers,
            "image_url": image_url,
        },
    }
    return render(request, "profile.html", context)


def welcome_page(request):
    return render(request, "index.html")


@login_required
def books_history(request):
    query = Books.objects.filter(user_id=request.user).all()
    dates = {}
    for book in query:
        date = (
            str(book.created_at.year)
            + "-"
            + str(book.created_at.month)
            + "-"
            + str(book.created_at.day)
        )
        if date not in dates.keys():
            dates[date] = []
        dates[date].append(
            {
                "title": book.title,
                "author": book.author,
                "summary": book.summary,
                "image_url": book.image_url,
            }
        )
    for date in dates:
        dates[date] = list({book["title"]: book for book in dates[date]}.values())

    context = {
        "dates": dates,
        "active_tab": "history", 
    }
    print(len(dates))
    return render(request, "history.html", context)


@login_required()
def favourites(request):
    current_user = User.objects.filter(id=request.user.id)[0]
    # ahed here im using raw sql, is this vulanerable to sql injection
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM blu_track WHERE user_id = " + str(request.user.id))

    refresh_token(request)
    access_token = request.session["access_token"]

    response = get(
        url="https://api.spotify.com/v1/me/top/tracks",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        },
        params={
            "limit": "30",
            
        },
    )

    artist_response = get(
        url="https://api.spotify.com/v1/me/top/artists",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        },
        params={
            "limit": "10",
        },
    )

    top_tracks = response.json().get("items")
    top_artists = artist_response.json().get("items")

    tracks = []
    artists = []
    for ar in top_artists:
        artist = {
            "name": ar["name"],
            "genres": [genre for genre in ar["genres"]],
            "image_url": ar["images"][0]["url"],
        }
        artists.append(artist)
    for track in top_tracks:
        single_track = {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "image_url": track["album"]["images"][0]["url"],
        }
        tracks.append(single_track)

    # saves data in the database with user_id
    to_be_saved = tracks
    for track in to_be_saved:
        track["user"] = current_user
    Track.objects.bulk_create([Track(**track) for track in to_be_saved])

    context = {
        "active_tab": "favourites",
        "tracks": tracks,
        "artists": artists,
    }
    # return tracks without user id
    return render(request, "favourites.html", context)


def get_books_from_lyrics(request, username):
    track_lyrics = fetch_lyrics(request, username)

    # load model and the vectorizer
    model = tf.keras.models.load_model(os.path.join(settings.BASE_DIR, "models\model2"))
    vectorizer = joblib.load(os.path.join(settings.BASE_DIR, "models\\vectorizer.pkl"))
    books = pd.read_csv(
        os.path.join(settings.BASE_DIR, r"ML_newdata\\all_data\books_predicted.csv")
    )

    # predict using models
    tracks_to_be_predicted = []
    for track in track_lyrics:
        if track != '':
            tracks_to_be_predicted.append(track)
    print(tracks_to_be_predicted)
    # fetch the lyrics
    predictions = []
    for track in tracks_to_be_predicted:
        track = vectorizer.transform([track]).toarray()
        prediction = model.predict(track)
        predictions.append(prediction[0])

    sim_vector = []
    songs = pd.DataFrame(predictions)

    for i in range(11):
        sim_vector.append(songs[i].mean())
    dic = {}

    for index, book in books.iterrows():
        clean = book.summary_predict
        clean = clean[2 : len(clean) - 2].split()
        clean = [float(s) for s in clean]
        cosine = np.dot(np.array(sim_vector), np.array(clean)) / (
            norm(np.array(sim_vector)) * norm(np.array(clean))
        )
        dic[index] = f"{(cosine * 100):.2f}"

    sorted_dict = {
        k: v for k, v in sorted(dic.items(), key=lambda item: item[1], reverse=True)
    }

    top_5 = dict(itertools.islice(sorted_dict.items(), 5))
    # print(categories)
    # print(random30)

    returned_books = []
    for key in top_5.keys():
        bok = books.name[key]
        author = books.autho[key]
        summary = books.summary[key]
        url = get_book_cover_image(bok, author)
        if url:
            image_url = get_book_cover_image(bok, author)
        else:
            image_url= "../static/default_book_image.png"

        isbn = get_isbn(bok, author)
        if isbn:
            isbn = get_isbn(bok, author)
        else:
            isbn = "unknown"
            
        if pd.isna(bok):
            bok = "unknown"
        if pd.isna(author):
            author = "unknown"
        if pd.isna(summary):
            summary = "unknown"

        book = {
            "name": bok,
            "author": author,
            "summary": summary,
            "image_url": image_url,
            "isbn":isbn,
        }
        returned_books.append(book)

    created_at = timezone.now()

    for book in returned_books:
        Books.objects.create(
            user_id=User.objects.filter(username=username)[0],
            title=book["name"],
            author=book["author"],
            summary=book["summary"],
            created_at=created_at,
            image_url=book["image_url"],
        ).save()

    # clear returned books
    jsonResponse = json.dumps(returned_books)

    return JsonResponse({"books": jsonResponse})


@login_required()
def predict(request):
    username = User.objects.filter(id=request.user.id)[0].username

    context = {
        "active_tab": "predict",
        "username": username,
    }
    return render(request, "predict.html", context)


@login_required()
def export_data(request):
    books = Books.objects.filter(user_id=request.user.id)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="books.csv"'

    writer = csv.writer(response)
    writer.writerow(["Title", "Author", "Summary", "Created At"])

    for book in books:
        created_at_local = book.created_at.astimezone(timezone.get_current_timezone())
        created_at_str = created_at_local.strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([book.title, book.author, book.summary, created_at_str])

    return response
