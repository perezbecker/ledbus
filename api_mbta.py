import urllib.request
import json
from datetime import datetime

def get_mbta_departures(stop_id):
    # MBTA API URL
    url = f"https://api-v3.mbta.com/predictions?filter%5Bstop%5D={stop_id}"
    
    # Make the API request
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)  # Parse the JSON response
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {
            "prediction_time": datetime.now().replace(tzinfo=None),
            "next_departure_time": None,
            "following_departure_time": None,
        }
    
    # Extract departure times
    departure_times = []
    for prediction in data.get("data", []):
        attributes = prediction.get("attributes", {})
        departure_time = attributes.get("departure_time")
        
        if departure_time:
            try:
                # Parse the ISO 8601 string into a datetime object
                departure_datetime = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S%z")
                # Strip timezone information
                departure_times.append(departure_datetime.replace(tzinfo=None))
            except ValueError as ve:
                print(f"Error parsing time: {ve}")
    
    # Prepare the return dictionary
    if len(departure_times) >= 2:
        return {
            "prediction_time": datetime.now().replace(tzinfo=None),  # Current time with no timezone
            "next_departure_time": departure_times[0],
            "following_departure_time": departure_times[1],
        }
    elif len(departure_times) == 1:
        return {
            "prediction_time": datetime.now().replace(tzinfo=None),
            "next_departure_time": departure_times[0],
            "following_departure_time": None,
        }
    else:
        return {
            "prediction_time": datetime.now().replace(tzinfo=None),
            "next_departure_time": None,
            "following_departure_time": None,
        }

if __name__ == "__main__":
    print("Testing Bus Departure Time API call:")
    print(get_mbta_departures(8674))
    print("Testing T Departure Time API call:")
    print(get_mbta_departures(70079))
