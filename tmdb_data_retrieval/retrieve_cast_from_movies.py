import os
import json
import time
import requests
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the bearer token from environment variable
bearer_token = os.getenv('TMDB_APIKEY')

# Define the headers for the request
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json;charset=utf-8'
}

# Load all the action movies data from the file
with open('./cache/all_action_movies_data_2022.json', 'r') as f:
    all_movies = json.load(f)

# For each movie, get the cast and add it to the movie data
for movie in all_movies:
    movie_id = movie['id']

    # Define the API URL
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'

    # Make the request
    response = requests.get(url, headers=headers)

    # Parse the JSON response
    data = response.json()

    # Add the cast to the movie data
    movie['cast'] = data['cast']

    print(f"Retrieved cast for movie: {movie['title']}")

    # Wait for a quarter of a second to avoid hitting rate limit
    time.sleep(0.25)

# Save all the data to a file
with open('./cache/all_action_movies_with_cast_data_2022.json', 'w') as f:
    json.dump(all_movies, f)
