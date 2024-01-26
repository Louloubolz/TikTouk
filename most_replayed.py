import requests
from urllib.parse import urlparse, parse_qs
import pandas as pd

def get_most_viewed(yt_link):

    # Parse the URL
    parsed_url = urlparse(yt_link)

    # Extract the video ID from the query parameters
    video_id = parse_qs(parsed_url.query).get("v", [])[0] if "v" in parse_qs(parsed_url.query) else None

    if not video_id:
        print("Unable to extract video ID from the URL.")
   
    api_url = "https://yt.lemnoslife.com/videos"
    params = {
        "part": "mostReplayed",
        "id": video_id
    }

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        # The request was successful
        data = response.json()
        markers = data["items"][0]["mostReplayed"]["markers"]
        most_viewed = [element for element in markers if element["intensityScoreNormalized"] > 0.8]
        print(most_viewed)
    else:
        # The request failed
        print(f"Error: {response.status_code} - {response.text}")

get_most_viewed("https://www.youtube.com/watch?v=dWbPdqns5Xk")