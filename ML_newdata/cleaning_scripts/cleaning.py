import pandas as pd
import numpy as np
import re
from langdetect import detect
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

data = pd.read_csv("tcc_ceds_music.csv")

data = data.sample(frac=1)
# data = pd.read_csv("23krecords_cleaned.csv")

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


processed = []
for lyric in data.lyrics:
    lyric = preprocess(lyric)
    processed.append(lyric)

data["lyrics_cleaned"] = processed

data["lyrics_cleaned"].replace("", np.nan, inplace=True)

data.dropna(subset=["lyrics_cleaned"], inplace=True)


lemmatizer = WordNetLemmatizer()
data["lyrics_cleaned"] = data["lyrics_cleaned"].apply(
    lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()])
)

    
data.drop(columns=[data.columns[0]], axis=1, inplace=True)
with open("cleaned.csv", "w+", encoding="utf8") as file:
    file.write(data.to_csv())
