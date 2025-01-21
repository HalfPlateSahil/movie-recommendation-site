import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the dataset
print("Loading dataset...")
movies = pd.read_csv("movies.csv")
movies["genres"] = movies["genres"].fillna("")  # Replace NaN genres with empty strings

# Helper function to get recommendations based on user preferences
def get_recommendations(mood, genre, companions):
    print(f"Received preferences - Mood: {mood}, Genre: {genre}, Companions: {companions}")
    
    # Mood to genre mapping
    mood_keywords = {
        "happy": ["Comedy", "Adventure"],
        "sad": ["Drama"],
        "excited": ["Action", "Adventure"],
        "romantic": ["Romance"],
        "adventurous": ["Action", "Adventure"]
    }
    
    relevant_genres = mood_keywords.get(mood, [])
    print(f"Relevant genres for mood '{mood}': {relevant_genres}")
    
    # Filter movies by genre selected by the user
    filtered_movies = movies[movies["genres"].str.contains(genre, case=False, na=False)]
    print(f"Filtered movies by genre '{genre}': {filtered_movies.shape[0]} movies found")
    
    # If the mood is relevant, further filter based on mood genres
    if relevant_genres:
        filtered_movies = filtered_movies[filtered_movies["genres"].str.contains('|'.join(relevant_genres), case=False)]
    print(f"Filtered movies after considering mood genres: {filtered_movies.shape[0]} movies found")
    
    # Further filter based on companions (you can adjust the logic here)
    if companions == "friends":
        filtered_movies = filtered_movies[filtered_movies["genres"].str.contains("Comedy|Action", case=False)]
    elif companions == "family":
        filtered_movies = filtered_movies[filtered_movies["genres"].str.contains("Animation|Family|Comedy", case=False)]
    elif companions == "alone":
        # No extra filter for watching alone
        pass

    print(f"Filtered movies based on companions '{companions}': {filtered_movies.shape[0]} movies found")
    
    # Limit to top 3 movie recommendations
    recommendations = filtered_movies.head(3)["title"].tolist()
    print(f"Recommendations: {recommendations}")
    
    return recommendations

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    # Get form data
    mood = request.form.get("mood")
    genre = request.form.get("genre")
    companions = request.form.get("companions")
    
    # Print form data for debugging
    print(f"Form data - Mood: {mood}, Genre: {genre}, Companions: {companions}")
    
    # Get recommendations based on preferences
    recommendations = get_recommendations(mood, genre, companions)
    
    # Return the recommendations to the user
    return render_template("index.html", recommendations=recommendations, mood=mood, genre=genre, companions=companions)

if __name__ == "__main__":
    app.run(debug=True)