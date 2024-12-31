from datetime import datetime


def get_ezride_departures(station_id):
    return {
        "prediction_time": datetime.now().replace(tzinfo=None),  # Current time with no timezone
        "next_departure_time": None,
        "following_departure_time": None,
        }