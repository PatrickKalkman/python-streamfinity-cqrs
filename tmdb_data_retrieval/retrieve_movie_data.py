import os
import json
import time
from dotenv import load_dotenv
import requests

# Load the .env file
load_dotenv()

# Get the bearer token from environment variable
bearer_token = os.getenv('TMDB_APIKEY')

# Define the headers for the request
headers = {
    'Authorization': f'Bearer {bearer_token}',
    'Content-Type': 'application/json;charset=utf-8'
}

# Define the base API URL for action movies from 2022
base_url = 'https://api.themoviedb.org/3/discover/movie?with_genres=28&primary_release_year=2022'

# Start with the first page
page_number = 1
all_data = []

# Loop to get data from all pages
while True:
    # Define the API URL for the current page
    url = f'{base_url}&page={page_number}'

    # Make the request
    response = requests.get(url, headers=headers, timeout=10)

    # Parse the JSON response
    data = response.json()

    # Add the results to all_data
    all_data.extend(data['results'])

    # If this is the last page, break the loop
    if page_number >= data['total_pages']:
        break

    # Otherwise, move to the next page
    page_number += 1

    print(f"retrieving page {page_number} of {data['total_pages']}")

    # Wait for a quarter of a second to avoid hitting rate limit
    time.sleep(0.25)

# Save all the data to a file
with open('./cache/all_action_movies_data_2022.json', 'w') as f:
    json.dump(all_data, f)
