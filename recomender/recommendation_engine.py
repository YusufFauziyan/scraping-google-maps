import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os

# Load data
csv_file_path = os.path.join(os.getcwd(), "data", "cleaned_coffee_data.csv")
df = pd.read_csv(csv_file_path)

# Gabungkan semua informasi yang ingin digunakan untuk rekomendasi
df["combined_text"] = df["name"] + " " + df["address"] + " " + df["rating"].astype(str)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(df["combined_text"])

# Hitung cosine similarity antar coffee shop
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Buat mapping index ke nama
indices = pd.Series(df.index, index=df["name"]).drop_duplicates()

def get_recommendations(name, top_n=5):
    idx = indices.get(name)
    if idx is None:
        return []

    sim_scores = list(enumerate(cosine_sim[idx].tolist()))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]

    recommendations = [df["name"].iloc[i[0]] for i in sim_scores]
    return recommendations

# Contoh
if __name__ == "__main__":
    nama_kopi = "Like Earth Coffee"
    rekomendasi = get_recommendations(nama_kopi)
    print(f"Rekomendasi untuk {nama_kopi}:")
    for r in rekomendasi:
        print("-", r)
