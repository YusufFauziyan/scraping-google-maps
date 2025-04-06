import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import os

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="coffee_recommender"
)

# Ambil data dari tabel
df = pd.read_sql("SELECT id, name, address, rating FROM coffee_shops", conn)
conn.close()

# Gabungkan kolom teks untuk vektorisasi
df["combined_text"] = df["name"] + " " + df["address"]

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words=None, lowercase=True, max_features=1000)
tfidf_matrix = vectorizer.fit_transform(df["combined_text"])

# Simpan vektor dan data
os.makedirs("model", exist_ok=True)
with open("model/tfidf_matrix.pkl", "wb") as f:
    pickle.dump(tfidf_matrix, f)

with open("model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

df.to_csv("data/cleaned_coffee_data.csv", index=False)
print("✅ Dataset siap digunakan untuk model rekomendasi!")
