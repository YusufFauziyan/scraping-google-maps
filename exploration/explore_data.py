import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Koneksi ke database
engine = create_engine("mysql+mysqlconnector://root:root@localhost:3306/coffee_recommender")

# Ambil data dari tabel
df = pd.read_sql("SELECT * FROM coffee_shops", engine)

# Lihat 5 data teratas
print(df.head())

# Bersihkan rating (ubah ke float)
df["rating_clean"] = df["rating"].str.replace(",", ".").str.extract(r'(\d+\.\d+|\d+)').astype(float)

# Cek distribusi rating
sns.histplot(df["rating_clean"].dropna(), bins=10, kde=True)
plt.title("Distribusi Rating Coffee Shop di Sukabumi")
plt.xlabel("Rating")
plt.ylabel("Jumlah Coffee Shop")
plt.tight_layout()
plt.show()
