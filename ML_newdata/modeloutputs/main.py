import pandas as pd
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from langdetect import detect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix
import joblib


stop_words = set(stopwords.words("english"))


# Load the data
data = pd.read_csv("..\\all_data\\cleaned.csv")
data = data.head(20000)
vectorizer = joblib.load("vectorizer.pkl")
# Split the data into train and test sets
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

# Apply preprocessing to train and test data
lyrics_train_preprocessed = lyrics_train
lyrics_test_preprocessed = lyrics_test

# Vectorize the preprocessed lyrics
lyrics_train_vectorized = vectorizer.transform(lyrics_train_preprocessed).toarray()
lyrics_test_vectorized = vectorizer.transform(lyrics_test_preprocessed).toarray()



# Assuming you have already loaded and preprocessed the test data
model = load_model("model2")
# Get model predictions
predictions = model.predict(lyrics_test_vectorized)
# Convert predictions to binary values (0 or 1) based on a threshold (e.g., 0.5)

# Get the label names
label_names = labels_test.columns
from sklearn.metrics import recall_score, accuracy_score, f1_score
from sklearn.preprocessing import Binarizer

# Assuming you have already trained the model and obtained predictions

# Convert predictions to binary values (0 or 1) based on a threshold (e.g., 0.5)
binary_predictions = np.where(predictions >= .909, 1, 0)
# Get the label names
label_names = labels_test.columns

# Binarize continuous labels
binarizer = Binarizer(threshold=0.5)  # Adjust the threshold as needed
labels_test_binary = binarizer.transform(labels_test)

# Calculate recall for each class
recalls = []
for i, label in enumerate(label_names):
    true_labels = labels_test_binary[:, i]
    predicted_labels = binary_predictions[:, i]
    recall = recall_score(true_labels, predicted_labels)
    recalls.append(recall)

# Calculate overall loss and accuracy
loss, accuracy = model.evaluate(lyrics_test_vectorized, labels_test_binary)

# Calculate F1 score for each class
f1_scores = []
for i, label in enumerate(label_names):
    true_labels = labels_test_binary[:, i]
    predicted_labels = binary_predictions[:, i]
    f1 = f1_score(true_labels, predicted_labels)
    f1_scores.append(f1)

# Print evaluation metrics
for label, recall, f1 in zip(label_names, recalls, f1_scores):
    print(f"Metrics for {label}:")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

print(f"Overall Loss: {loss:.4f}")
print(f"Overall Accuracy: {accuracy:.4f}")
