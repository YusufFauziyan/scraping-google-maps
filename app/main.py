from flask import Flask, jsonify
from api.routes import api  # Blueprint dari routes.py

app = Flask(__name__)

# Semua route akan diawali dengan /api
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

