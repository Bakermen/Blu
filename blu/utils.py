from .models import Track
from lyricsgenius import Genius
from langdetect import detect
from nltk.corpus import stopwords
from .models import *
from dotenv import load_dotenv
import requests
import os
import re


load_dotenv()
stop_words = set(stopwords.words("english"))


def preprocess(text):
    if detect(text) != "en":
        return ""
    text = text.replace(",", "").replace(".", "").replace('"', "").replace("'", "")
    lowered = text.lower()

    stopwords_removed = " ".join(
        [word for word in lowered.split() if word not in stop_words]
    )
    return stopwords_removed


# utils
def fetch_lyrics(request, username):
    tracks = Track.objects.filter(user=User.objects.filter(username=username)[0]).all()
    genius = Genius(
        os.getenv("genuis_token"),
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
        remove_section_headers=True,
        timeout=120,
    )
    all_lyrics = []
    for track in tracks:
        while True:
            try:
                song = genius.search_song(track.name, artist=track.artist)
            except ValueError:
                print(ValueError)
                continue
            else:
                break
        if song:
            if detect(song.lyrics) == "en":
                lyrics = song.lyrics.replace("\n", " ").split(" ")
                if len(lyrics) > 950:
                    lyrics = " "
                else:
                    i = 0
                    while "Lyrics" not in lyrics[i]:
                        i += 1
                    lyrics[-1] = lyrics[-1][:-5]
                    lyrics[-1] = re.sub("[^A-Za-z]+", "", lyrics[-1])
                    lyrics = " ".join(lyrics[i + 1 :])
                    re.sub(r"\r|\x0b|\x0c", "", lyrics)
                    preprocess(lyrics)
            else:
                lyrics = ""
        else:
            lyrics = ""
        all_lyrics.append(lyrics)
    return all_lyrics


def get_book_cover_image(book_title, author):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": book_title, "a": author}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "items" in data:
            items = data["items"]
            if items:
                # Extract the image link from the first item
                image_link = (
                    items[0]["volumeInfo"].get("imageLinks", {}).get("thumbnail")
                )
                return image_link
        return "../static/default_book_image.png"
    except:
        return "../static/default_book_image.png"
    
def get_isbn(book_title, author):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": book_title, "a": author}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "items" in data:
            items = data["items"]
            if items:
                isbn = items[0]["volumeInfo"].get("industryIdentifiers")[1]["identifier"]
                return isbn
        return "unknown"
    except:
        return "unknown"
