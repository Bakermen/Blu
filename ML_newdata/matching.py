import pandas as pd
import numpy as np
from numpy.linalg import norm
import ast
import itertools

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


books = pd.read_csv("all_data/books_predicted.csv")
songs = pd.read_csv("all_data/cleaned.csv")

random30 = songs.sample(n=30).reset_index()
sim_vector = []

for cat in categories:
    sim_vector.append(random30[cat].mean())
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
print(top_5)
for key in top_5.keys():
    bok = books[" name"][key]
    author = books[" autho"][key]
    summary = books[" summary"][key]
    print(bok, author)

# first_book = books.summary_predict[0]
# first_book =  (first_book[2:len(first_book)-2].split())
# first_book = [float(book) for book in first_book]


# cosine = np.dot(np.array(sim_vector),np.array(first_book))/(norm(np.array(sim_vector))*norm(np.array(first_book)))
