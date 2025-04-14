---

# ☕️ SCRAPING-GOOGLE-MAPS

This project is a Python-based application designed to scrape coffee shop data from Google Maps, clean and prepare the data, and build a recommendation system using TF-IDF and cosine similarity.

---

## 📁 Project Structure

```
SCRAPING-GOOGLE-MAPS/
├── app/
│   ├── api/
│   │   ├── routes.py               # API routing logic
│   │   └── __init__.py
│   └── core/
│       ├── config.py               # Configuration (env, constants, etc)
│       └── __init__.py
│
├── scraping/
│   ├── coffee_scraper.py          # Google Maps coffee shop scraper
│   └── __init__.py
│
├── scripts/
│   ├── prepare_dataset.py         # Cleaning and preprocessing raw data
│   ├── recomendation_coffe_shop.py# Recommendation logic based on TF-IDF
│   ├── main.py                    # Main script runner
│   └── __init__.py
│
├── data/
│   ├── coffe_raw.json             # Raw scraped JSON data
│   └── cleaned_coffee_data.csv    # Cleaned and structured CSV data
│
├── model/
│   ├── tfidf_matrix.pkl           # Pickled TF-IDF matrix
│   └── vectorizer.pkl             # Pickled TF-IDF vectorizer
│
├── .env                           # Environment variables
├── .env.example                   # Template for env variables
├── docker-compose.yml             # Docker configuration (optional)
├── postman_collection.json        # Example API call (import to posmman)
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## ⚙️ Features

- ✅ Scrape coffee shops from Google Maps (name, address, rating, reviews, etc)
- ✅ Clean and normalize scraped data
- ✅ Store clean data in CSV and raw in JSON
- ✅ Generate TF-IDF based vector representations
- ✅ Recommend coffee shops based on similarity & popularity
- ✅ Score by normalized rating + review count (60:40 weight)

---

## 🚀 How to Run

### 1. Clone this repository
```bash
git clone https://github.com/your-username/SCRAPING-GOOGLE-MAPS.git
cd SCRAPING-GOOGLE-MAPS
```

### 2. Create & configure environment
```bash
cp .env.example .env
# Edit .env file to set your API keys (if needed)
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the main script
```bash
python scripts/main.py
```

---

## 🧠 How Recommendation Works

- **Text Features**: Combines name, address, and rating into text format.
- **TF-IDF**: Transforms text into vectors using `TfidfVectorizer`.
- **Cosine Similarity**: Measures similarity between vectorized coffee shops.
- **Popularity Score**: Calculated using a weighted average of rating and reviews.

```python
score = ((rating_norm * 0.6) + (reviews_norm * 0.4)) * 100
```

Final results are sorted by score and returned as JSON-friendly data (array of objects).

---

## 📝 Example Output

```json
[
  {
    "name": "Kopi Nako Sukabumi",
    "address": "Jl. Mayor Mahmud",
    "rating": "4,9",
    "total_reviews": 2292,
    "latitude": -6.90501,
    "longitude": 106.942,
    "link": "https://...",
    "score": 100
  },
  ...
]
```

---

## 📦 Docker Support

You can optionally use Docker with the provided `docker-compose.yml` file (if configured).

---

## 📌 Requirements

- Python 3.8+
- `pandas`, `scikit-learn`, `numpy`, `requests`, etc.

> All dependencies are listed in `requirements.txt`

---