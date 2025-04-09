import mysql.connector
import os
import json
from dotenv import load_dotenv

def get_mysql_connection():
    """Establish a MySQL database connection."""
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error MySQL: {e}")
        exit(1)


def load_json_data(filename: str):
    """Load JSON data from a given file path."""
    json_file_path = os.path.join(os.getcwd(), "data", filename)
    print(f"Find Json file in: {json_file_path}")

    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"Total data will insert: {len(data)}")

        if not data:
            raise ValueError("JSON file is empty. Please check the scraping process!")

        return data

    except FileNotFoundError:
        print("Error: JSON file not found. Please run the scraping script first!")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format!")
        exit(1)


def setup_and_insert_data():
    # read from json file
    coffee_data = load_json_data("coffe_raw.json")


    """Create table, clear old data, and insert new coffee shop data."""
    conn = get_mysql_connection()
    try:
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS coffee_shops (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address TEXT,
                rating VARCHAR(10),
                latitude FLOAT,
                longitude FLOAT,
                link VARCHAR(255),
                total_reviews INT,
                opening_hours TEXT,
                phone VARCHAR(50)
            )
        """)
        
        print("Table coffee_shops was created.")

        # Delete old data
        cursor.execute("DELETE FROM coffee_shops")
        print("All Data was deleted.")

        # Insert new data
        for item in coffee_data:
            # Check if essential fields are present (e.g., name)
            # if item["name"] in [None, "N/A", ""]:
            #     print(f"Skipping incomplete data: {item["link"]}")
            #     continue  # Skip this item
            
            try:
                cursor.execute("""
                    INSERT INTO coffee_shops (name, address, rating, latitude, longitude, link, total_reviews, opening_hours, phone)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    item.get("name"),
                    item.get("address"),
                    item.get("rating") or None,  # Use None if rating is empty
                    float(item["latitude"]) if isinstance(item["latitude"], str) else item["latitude"],  # Convert to float if it's a string
                    float(item["longitude"]) if isinstance(item["longitude"], str) else item["longitude"],
                    item.get("link") or None,  # Use None if link is empty
                    item.get("total_reviews") or 0,  # Default to 0 if missing
                    item.get("opening_hours") or None,
                    item.get("phone") or None
                ))
            except Exception as e:
                print(f"Error inserting data: {item['name']}, error: {e}")


        conn.commit()
        print(f"Successfully inserted {cursor.rowcount} records into coffee_shops table.")

    except mysql.connector.Error as e:
        print(f"Error when insert data: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()