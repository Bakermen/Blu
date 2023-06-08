import pandas as pd
import numpy as np
import re
from langdetect import detect
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

data = pd.read_csv("books.csv")

stop_words = set(stopwords.words("english"))
data[" summary"].replace("", np.nan, inplace=True)

data.dropna(subset=[" summary"], inplace=True)



def preprocess(text):
    
    text = text.replace(",", "").replace(".", "").replace('"', "").replace("'", "").replace("#" , "").replace("\\", "")
    lowered = text.lower()

    stopwords_removed = " ".join(
        [word for word in lowered.split() if word not in stop_words]
    )
    return stopwords_removed
print(data.columns)

processed = []
for lyric in data[" summary"]:
    lyric = preprocess(lyric)
    processed.append(lyric)

data["summary_cleaned"] = processed

data["summary_cleaned"].replace("", np.nan, inplace=True)

data.dropna(subset=["summary_cleaned"], inplace=True)


lemmatizer = WordNetLemmatizer()
data["summary_cleaned"] = data["summary_cleaned"].apply(
    lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()])
)

    
#data.drop(columns=[data.columns[0]], axis=1, inplace=True)

with open("cleaned_books.csv", "w+", encoding="utf8") as file:
    file.write(data.to_csv())
