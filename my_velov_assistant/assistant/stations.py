import json
import os
import urllib.request
from dataclasses import dataclass
from typing import List

from my_velov_assistant.assistant.point import Point

DECAUX_API_KEY = os.environ["DECAUX_API_KEY"]
DECAUX_API_URL = os.environ["DECAUX_API_URL"]


@dataclass
class Station:
    """Definition of a velov station"""

    number: int
    name: str
    position: Point
    free_bike: int
    free_place: int


# type alias for type hinting
Stations = List[Station]


def get_stations(city: str = "lyon") -> Stations:
    """Returns the list of the velov stations filtered by the city."""

    url = f"{DECAUX_API_URL}?apiKey={DECAUX_API_KEY}"
    response = urllib.request.urlopen(url)
    stations = json.loads(response.read().decode())

    # filtering using the city parameter
    return [
        Station(
            number=s["number"],
            name=s["name"],
            position=Point(s["position"]["latitude"], s["position"]["longitude"]),
            free_bike=s["mainStands"]["availabilities"]["bikes"],
            free_place=s["mainStands"]["availabilities"]["stands"],
        )
        for s in stations
        if s["contractName"] == city
    ]
