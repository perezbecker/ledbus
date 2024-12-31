from datetime import datetime


def get_blue_bikes_station_info(station_id):
    return {
        "prediction_time": datetime.now().replace(tzinfo=None),  # Current time with no timezone
        "bikes_available": 5,
        "parking_spaces_available": 3,
        }