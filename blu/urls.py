from django.urls import path
from . import views


app_name = "blu"

urlpatterns = [
    path("", views.welcome_page, name="welcome"),
    path("profile", views.user_info, name="profile"),
    path("favourites/", views.favourites, name="favourites"),
    path("history/", views.books_history, name="history"),
    path("BLU/", views.predict, name="predict"),
    path("get_books/<str:username>", views.get_books_from_lyrics, name="get_books"),
    path("export_data", views.export_data, name="export"),
]
