import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os
from core import get_mysql_connection

def prepare_dataset():
    # Connection to MySQL database
    conn = get_mysql_connection()

    # Get data from MySQL
    df = pd.read_sql("SELECT id, name, address, rating, latitude, longitude, link, total_reviews, opening_hours, phone   FROM coffee_shops", conn)
    conn.close()

    # Combine name and address for TF-IDF
    df["combined_text"] = df["name"] + " " + df["address"]

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words=None, lowercase=True, max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df["combined_text"])

    # Save TF-IDF matrix and vectorizer
    os.makedirs("model", exist_ok=True)
    with open("model/tfidf_matrix.pkl", "wb") as f:
        pickle.dump(tfidf_matrix, f)

    with open("model/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)

    df.to_csv("data/cleaned_coffee_data.csv", index=False)
    print("✅ Dataset was ready to use.")
