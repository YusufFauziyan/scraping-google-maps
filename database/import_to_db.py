import json
import mysql.connector
import os

# 1. Pastikan path file JSON benar
json_file_path = os.path.join(os.getcwd(), "data", "sukabumi_coffee_raw.json")  # Gunakan path relatif
print(f"Mencari file JSON di: {json_file_path}")

# 2. Baca file JSON
try:
    with open(json_file_path, "r", encoding="utf-8") as f:
        coffee_data = json.load(f)
    print(f"Jumlah data yang akan dimasukkan: {len(coffee_data)}")
    
    if not coffee_data:
        raise ValueError("File JSON ada tetapi kosong. Pastikan scraping berhasil!")

except FileNotFoundError:
    print("Error: File JSON tidak ditemukan. Jalankan script scraping terlebih dahulu!")
    exit(1)
except json.JSONDecodeError:
    print("Error: Format JSON tidak valid!")
    exit(1)

# 3. Koneksi ke MySQL
try:
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="coffee_recommender"
    )
    cursor = conn.cursor()

    # 4. Buat tabel jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coffee_shops (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            address TEXT,
            rating VARCHAR(10)
        )
    """)

    # 5. Hapus semua data lama sebelum insert ulang
    cursor.execute("DELETE FROM coffee_shops")
    print("Semua data lama dihapus.")

    # 6. Masukkan data baru
    for item in coffee_data:
        cursor.execute("""
            INSERT INTO coffee_shops (name, address, rating)
            VALUES (%s, %s, %s)
        """, (item["name"], item["address"], item["rating"]))

    conn.commit()
    print(f"Berhasil menyimpan ulang {len(coffee_data)} data ke dalam database!")

except mysql.connector.Error as e:
    print(f"Error MySQL: {e}")
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
