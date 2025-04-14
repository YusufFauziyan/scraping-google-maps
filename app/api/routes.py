from flask import Blueprint, jsonify, request
from core import get_mysql_connection, setup_and_insert_data
from scraping import scrape_coffee_shops
from scripts import prepare_dataset, get_top_rated_popular

api = Blueprint("api", __name__)

# api healt
@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "success", "message": "API is running"}), 200

@api.route("/connection", methods=["GET"])
def test_connection():
    try:
        conn = get_mysql_connection()
        if conn.is_connected():
            conn.close()
            return jsonify({"status": "success", "message": "Koneksi ke database berhasil"}), 200
        else:
            return jsonify({"status": "error", "message": "Gagal terkoneksi ke database"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# scrapping
@api.route("/scrape", methods=["GET"])
def scrape():
    query = request.args.get("query")

    if not query:
        query = "coffee+shop+di+Sukabumi,+Jawa+Barat"

    # Import the scraping function here to avoid circular imports
    try:
        scrape_coffee_shops(query)

        print(f"Scraping data for query: {query}")

        # insert data to database
        try:
            setup_and_insert_data()
            print(f"Data was inserted to database")

            try:
                prepare_dataset()

                return jsonify({"status": "success", "message": f"Success Scrapp Data {query}"}), 200
            except Exception as e:
                print(f"Error when preparing dataset: {e}")


        except Exception as e:
            print(f"Error when insert data: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500


        # return jsonify({"status": "success", "message": f"Success get data from {query.replace("+", " ")}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
# scrapping
@api.route("/recomendation", methods=["GET"])
def recomendations():

    limit = request.args.get("limit")

    if not limit:
        limit = 5

    # check if limit is not number
    if not limit.isdigit():
        return jsonify({"status": "error", "message": "Limit must be a number"}), 400

    limit = int(limit)

    try:
        top_coffee = get_top_rated_popular(limit)

        print(f"Get top coffee shop", top_coffee)

        return jsonify({"items": top_coffee}), 200
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500