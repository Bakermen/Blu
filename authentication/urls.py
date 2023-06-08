from django.urls import path,include
from . import views


app_name = "auth"
urlpatterns = [
    path("login", views.login, name="login"),
    path("callback", views.callback, name="callback"),
    path("logout", views.logout, name="logout"),
    path("",include('blu.urls'))
]
