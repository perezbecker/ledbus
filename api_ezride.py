import json
from datetime import datetime

def get_ezride_departures(stop_id):
    """
    Returns a dictionary of the form:
        {
            "prediction_time": datetime object (current time, no tz),
            "next_departure_time": datetime or None,
            "following_departure_time": datetime or None
        }
    
    Steps:
    1. Parse hard-coded times into datetime objects for today's date.
    2. Only keep departure times >= 'now'.
    3. Sort the remaining times.
    4. Compare each of the earliest two times against a 99-minute threshold:
         - If a departure is more than 99 minutes from now, set it to None.
         - Otherwise, keep the datetime object.
    5. Always return the dictionary with the final "next_departure_time" and
       "following_departure_time" (which may be None).
    """

    # Hard-coded departure times
    erie_morning_times = [
        "6:48", "6:58", "7:08", "7:18", "7:28", "7:38", "7:46", "7:54",
        "8:02", "8:10", "8:18", "8:26", "8:34", "8:42", "8:50", "8:58",
        "9:06", "9:14", "9:22", "9:30", "9:38", "9:46", "9:54", "10:03",
        "10:13", "10:23", "10:33", "10:43"
    ]

    erie_evening_times = [
        "14:55", "15:10", "15:20", "15:30", "15:40", "15:50", "16:00", "16:10",
        "16:20", "16:30", "16:40", "16:46", "16:54", "16:58", "17:06", "17:14",
        "17:22", "17:30", "17:38", "17:50", "17:58", "18:06", "18:14", "18:22",
        "18:30", "18:38", "18:48", "18:58", "19:08", "19:18", "19:28"
    ]

    # Current time (without timezone)
    now = datetime.now().replace(tzinfo=None)

    # Combine morning + evening times
    all_times = erie_morning_times + erie_evening_times

    # Parse times into datetime objects (today's date)
    parsed_departure_times = []
    for time_str in all_times:
        try:
            dt_time = datetime.strptime(time_str, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            parsed_departure_times.append(dt_time)
        except ValueError as ve:
            print("Error parsing time: {}".format(ve))

    # Filter out times in the past, then sort
    departure_times = [t for t in parsed_departure_times if t >= now]
    departure_times.sort()

    # Helper function to check if a time is within 99 minutes from now
    def is_within_99_minutes(future_time):
        return (future_time - now).total_seconds() / 60 <= 99

    # By default, set next_departure_time and following_departure_time to None
    next_departure_time = None
    following_departure_time = None

    # If we have at least one upcoming time
    if len(departure_times) >= 1:
        # Check if the earliest time is within 99 minutes
        if is_within_99_minutes(departure_times[0]):
            next_departure_time = departure_times[0]
        # otherwise, next_departure_time remains None

    # If we have at least two upcoming times
    if len(departure_times) >= 2:
        # Check if the second earliest time is within 99 minutes
        if is_within_99_minutes(departure_times[1]):
            following_departure_time = departure_times[1]
        # otherwise, following_departure_time remains None

    return {
        "prediction_time": now,
        "next_departure_time": next_departure_time,
        "following_departure_time": following_departure_time
    }

if __name__ == "__main__":
    # Dummy test
    print("Testing EZRide Departures with dummy stop_id 100:")
    print(get_ezride_departures(100))
