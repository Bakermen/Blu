# Blu
A musical preference book recommendation system using django and tensorflow
# Installation
## Install the source code
make sure that python is installed on the server (whichever version from 3.8 to 3.10) and make sure that pip is installed.

## Requirements file
Open your terminal inside the project’s path and make sure that you are running the terminal in the “SPOTIFY_ANALYSIS” parent directory and install the requirements for the project by using this command:
```bash
pip install -r requirements.txt
```

## Set up the database
  * you either make a .env file in the main project directory(Spotify_analysis), and fill it with the information needed for the database connection like this
    ```.env
    database = "[DATABASE NAME HERE]"
    user = "[DATABASE USER HERE]"
    password = "[CONNECTION PASSWORD HERE]"
    ```
  
  * or change the database connection back to default(sqlite3), by replacing the database settings in Spotify_analysis/settings.py like this:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```

## Spotify API
Log in to the Spotify developer platform using this link [Spotify Developer](https://developer.spotify.com/), On the newly logged into account go to the dashboard https://developer.spotify.com/dashboard , and create a new app, put in the desired app name, and the description for it, and use the redirect link: http://127.0.0.1:8000/authentication/callback, which is the local host Ip address and the port of which Django (our project) runs on by default, and the authentication slug is the name of the application within our project that is responsible for redirecting the user to the Spotify platform to login (callback) and give our service permissions to fetch their songs.

in the "authentication" app directory, create a .env file and fill it in with these informations:
```.env
client_id = “[YOUR GENERATED CLIENT_ID]”
client_secret = “[YOUR GENERATED CLIENT_SECRET]”
redirect_uri = “http://127.0.0.1:8000/authentication/callback“
```
## Downloading stopwords
And run the following command in bash:

```bash
> python

>>> import nltk
>>> nltk.download(“stopwords”)
>>> exit()
```
## Training the model
cd into the MachineLearning directory
```bash
cd ML_newdata
python ../ML_newdata/model.py
```
Make sure that a new folder has been created inside the folder you’re in, which is “models/”, and that new created folder name will be “model2”, and a pickle file with the name “vectorizer.pkl”.
## running the server
```bash
python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```
# License
[MIT](https://github.com/Bakermen/Blu/blob/main/LICENSE)
