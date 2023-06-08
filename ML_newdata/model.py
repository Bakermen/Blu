import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from langdetect import detect
from nltk.corpus import stopwords
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Dense,
    Dropout,
)

import joblib

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


# prettier ignore
data = pd.read_csv(
    r"all_data\\cleaned.csv"
)
data = data.head(20000)
lyrics_train, lyrics_test, labels_train, labels_test = train_test_split(
    data["lyrics_cleaned"],
    data[
        [
            "sadness",
            "world/life",
            "music",
            "romantic",
            "violence",
            "obscene",
            "night/time",
            "feelings",
            "family/gospel",
            "dating",
            "communication",
        ]
    ],
    test_size=0.2,
    random_state=42,
)
vectorizer = TfidfVectorizer()
lyrics_train_vectorized = vectorizer.fit_transform(lyrics_train).toarray()
lyrics_test_vectorized = vectorizer.transform(lyrics_test).toarray()

print(lyrics_train_vectorized.shape)

model = Sequential()
model.add(Dense(units=64, activation="relu"))
model.add(Dropout(rate=0.2))
model.add(Dense(units=32, activation="relu"))
model.add(Dense(units=labels_train.shape[1], activation="softmax"))
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(lyrics_train_vectorized, labels_train, epochs=30, batch_size=32)


loss, accuracy = model.evaluate(lyrics_test_vectorized, labels_test)
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")


tf.keras.models.save_model(model=model, filepath="../models/model2")
# text = "Old Major, the old boar on the Manor Farm, calls the animals on the farm for a meeting, where he compares the humans to parasites and teaches the animals a revolutionary song, 'Beasts of England'. When Major dies, two young pigs, Snowball and Napoleon, assume command and turn his dream into a philosophy. The animals revolt and drive the drunken and irresponsible Mr Jones from the farm, renaming it 'Animal Farm'. They adopt Seven Commandments of Animal-ism, the most important of which is, 'All animals are equal'. Snowball attempts to teach the animals reading and writing; food is plentiful, and the farm runs smoothly. The pigs elevate themselves to positions of leadership and set aside special food items, ostensibly for their personal health. Napoleon takes the pups from the farm dogs and trains them privately."
# text = preprocess(text)

# text = vectorizer.transform([text]).toarray()
categories = [
    "sadness",
    "world/life",
    "music",
    "romantic",
    "violence",
    "obscene",
    "night/time",
    "feelings",
    "family/gospel",
    "dating",
    "communication",
]
joblib.dump(vectorizer, "../models/vectorizer.pkl")
# prediction = model.predict(text)
# print(prediction[0])

# dd = pd.read_csv("cleaned_books.csv")
# predictions = []
# for summary in dd["summary_cleaned"]:
#     summary = vectorizer.transform([summary]).toarray()
#     pr = model.predict(summary)
#     predictions.append(pr)


# dd["summary_predict"] = predictions
# print(":)")
# dd.to_csv("books_predicted")
