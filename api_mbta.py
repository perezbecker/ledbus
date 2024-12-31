import urllib.request
import json
from datetime import datetime

def get_mbta_departures(stop_id):
    # MBTA API URL
    url = "https://api-v3.mbta.com/predictions?filter%5Bstop%5D="+str(stop_id)
    
    # Make the API request
    try:
        response = urllib.request.urlopen(url)
        response_content = response.read().decode('utf-8')
        data = json.loads(response_content)
        response.close()
    except Exception as e:
        print("Error fetching data: "+str(e))
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
                # Strip timezone information from the ISO 8601 string
                if "-" in departure_time:
                    departure_time = departure_time[:-6]
                elif "Z" in departure_time:
                    departure_time = departure_time.replace("Z", "")

                # Parse the ISO 8601 string into a datetime object
                departure_datetime = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S")
                departure_times.append(departure_datetime)
            except ValueError as ve:
                print("Error parsing time: {}".format(ve))

    
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
