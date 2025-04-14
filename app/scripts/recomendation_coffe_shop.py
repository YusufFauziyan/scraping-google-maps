import os
import pandas as pd

def get_top_rated_popular(top_n=5):
    # Load CSV data
    csv_file_path = os.path.join(os.getcwd(), "data", "cleaned_coffee_data.csv")
    df = pd.read_csv(csv_file_path)

    # Combine fields for text similarity (name + address + rating)
    df["combined_text"] = df["name"] + " " + df["address"] + " " + df["rating"].astype(str)
    
    """
    Get top coffee shops based on high rating and number of reviews
    """
    # Convert rating from string "4,9" to float 4.9
    df["rating_clean"] = df["rating"].str.replace(",", ".").astype(float)

    # Normalize rating and total_reviews
    df["rating_norm"] = (df["rating_clean"] - df["rating_clean"].min()) / (df["rating_clean"].max() - df["rating_clean"].min())
    df["reviews_norm"] = (df["total_reviews"] - df["total_reviews"].min()) / (df["total_reviews"].max() - df["total_reviews"].min())

    # Calculate final score with weights and round to nearest whole number
    df["score"] = ((df["rating_norm"] * 0.6 + df["reviews_norm"] * 0.4) * 100).round().astype(int)

    # Sort by score and return top N as array of objects
    top_recommendations = df.sort_values(by="score", ascending=False).head(top_n)
    # Drop 'id' column and convert to list of dictionaries
    return top_recommendations.drop(columns=["id"]).to_dict(orient="records")
