
from datetime import datetime
import time

import stops



from api_mbta import get_mbta_departures
from api_blue_bikes import get_blue_bikes_station_info
from api_ezride import get_ezride_departures

localdir="/mnt/usb/ledlogs/"

class MbtaStop:
    def __init__(self, stop):
        self.stop = stop
        self.departure_times = {}
        self.age_prediction = None
        self.formatted_departure_time = None
        self.refresh_predictions()

    def refresh_predictions(self):
        """
        Refreshes departure predictions by fetching new data.
        """
        self.departure_times = get_mbta_departures(self.stop['stop_id'])
        self.update_predictions()

    def update_predictions(self):
        """
        Updates prediction data and formats departure times.
        """
        prediction_time = self.departure_times.get("prediction_time")
        next_departure_time = self.departure_times.get("next_departure_time")
        following_departure_time = self.departure_times.get("following_departure_time")

        self.age_prediction = self.age_prediction_time_in_seconds(prediction_time)
        time_until_next_departure = self.time_until_departure_in_seconds(next_departure_time)
        time_until_following_departure = self.time_until_departure_in_seconds(following_departure_time)

        self.formatted_departure_time = self.format_time_until_departure(
            time_until_next_departure, time_until_following_departure
        )

    @staticmethod
    def age_prediction_time_in_seconds(prediction_time):
        """
        Calculates the age of the prediction in seconds.
        """
        now = datetime.now()
        return (now - prediction_time).total_seconds()

    @staticmethod
    def time_until_departure_in_seconds(departure_time):
        """
        Calculates the time until departure in seconds.
        """
        now = datetime.now()
        return (departure_time - now).total_seconds()

    @staticmethod
    def format_time_until_departure(next_departure_in_seconds, following_departure_in_seconds=None):
        """
        Formats the time until the next departure and determines the corresponding text and color.
        """
        departure_color_scheme = ["w", "g", "y", "y", "r", "r"]

        if following_departure_in_seconds is None:
            following_departure_color = "p"
        else:
            delta_dt = following_departure_in_seconds - next_departure_in_seconds
            if 0 < delta_dt < 1500:
                following_departure_color = departure_color_scheme[int(delta_dt / 300)]
            elif delta_dt >= 1500:
                following_departure_color = departure_color_scheme[5]
            else:
                following_departure_color = "b"

        fractional_minute_display = ["A", "B", "C", "D", "E", "F"]

        if next_departure_in_seconds < 0:
            following_departure_text = "<0"
        elif 0 <= next_departure_in_seconds < 600:
            following_departure_text = str(int(next_departure_in_seconds / 60))+fractional_minute_display[int((next_departure_in_seconds % 60) / 10)]
        elif 600 <= next_departure_in_seconds < 5940:
            following_departure_text = str(int(next_departure_in_seconds / 60))
        elif next_departure_in_seconds >= 5940:
            following_departure_text = "++"
        else:
            following_departure_text = "  "

        return (following_departure_text + following_departure_color).replace("0", "O")

    def __str__(self):
        """
        String representation for debugging.
        """
        return "MbtaStop(name={}, id={}, formatted_departure={})".format(
        self.stop['name'], self.stop['stop_id'], self.formatted_departure_time)



my_stops = stops.stops

transit_mode_objects = [MbtaStop(stop) for stop in my_stops]

while True:
    text_to_display=""
    for transit_mode in transit_mode_objects:
        if transit_mode.age_prediction is not None and transit_mode.age_prediction < 30:
            transit_mode.update_predictions()
        else:
            transit_mode.refresh_predictions()

        text_to_display = text_to_display+transit_mode.formatted_departure_time
        print(transit_mode)
    f = open(localdir+"predictions","w")
    f.write(text_to_display+"\n")
    f.close()
    time.sleep(2)

 


