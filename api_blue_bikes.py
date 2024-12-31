import urllib.request
import json
from datetime import datetime

def get_blue_bikes_station_info(station_id):
    # Blue Bikes API URL
    url = "https://gbfs.bluebikes.com/gbfs/en/station_status.json"

    try:
        # Make the API request
        response = urllib.request.urlopen(url)
        response_content = response.read().decode('utf-8')
        data = json.loads(response_content)
        response.close()

        # Extract the list of stations
        stations = data.get("data", {}).get("stations", [])

        # Find the station with the matching station_id
        for station in stations:
            if station.get("station_id") == station_id:
                last_reported = station.get("last_reported", 0)

                # Convert last_reported timestamp to a Python datetime object
                prediction_time = datetime.fromtimestamp(last_reported)

                return {
                    "prediction_time": prediction_time,
                    "num_bikes_available": station.get("num_bikes_available", 0),
                    "num_docks_available": station.get("num_docks_available", 0),
                }

        # Return None if the station_id is not found
        return None

    except Exception as e:
        print("Error fetching Blue Bikes data: " + str(e))
        return None

# Example usage
if __name__ == "__main__":
    print("Testing Blue Bikes API call:")
    station_info = get_blue_bikes_station_info("f8349e56-0de8-11e7-991c-3863bb43a7d0")
    if station_info:
        print(station_info)
    else:
        print("Station not found or data could not be retrieved.")