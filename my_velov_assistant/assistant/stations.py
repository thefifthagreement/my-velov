"""Dataclass and functions for the manipulation of the velov stations"""
import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Dict, List

from my_velov_assistant.assistant.point import Point, get_distance

DECAUX_API_KEY = os.environ["DECAUX_API_KEY"]
DECAUX_API_URL = os.environ["DECAUX_API_URL"]


@dataclass
class Station:
    """Definition of a velov station"""

    #: the station ID
    number: int
    #: the station name
    name: str
    #: the coordinates (lat, long) of the station
    position: Point
    #: the number of free bikes
    free_bike: int
    #: the number of free places
    free_place: int


#: type alias for type hinting
Stations = List[Station]


def get_stations(city: str = "lyon") -> Stations:
    """Returns the list of the velov stations filtered by the city.

    :param city: The city to filter the stations returned by the API
    :return: The list of station of the city
    """

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


def get_station(number: int, stations: Stations) -> Station:
    """Returns the station which ID is the number.

    :param number: The number of the station to find
    :param stations: The list of stations
    :return: The station with the same number or None
    """

    station: Station = None
    for s in stations:
        if s.number == number:
            station = s
            break
    return station


def get_nearest_station(distances: Dict[int, float], stations: Stations):
    """Returns the nearest station using the distances

    :param distances: A dict of number -> distance
    :param stations: The list of velov stations
    :return: The nearest station
    """

    nearest = sorted(distances.items(), key=lambda x: x[1])[0]
    return get_station(nearest[0], stations)


def get_nearest_free_bike(position: Point, stations: Stations) -> Station:
    """Returns the nearest station from the position with a free bike

    :param position: The position of the user
    :param stations: The list of veloc stations
    :return: The nearest station with a free bike
    """

    distances = {
        s.number: get_distance(position, s.position)
        for s in stations
        if s.free_bike > 0
    }
    return get_nearest_station(distances, stations)


def get_nearest_free_place(position: Point, stations: Stations) -> Station:
    """Returns the nearest station from the position with a free place

    :param position: The position of the user
    :param stations: The list of veloc stations
    :return: The nearest station with a free place
    """

    distances = {
        s.number: get_distance(position, s.position)
        for s in stations
        if s.free_place > 0
    }
    return get_nearest_station(distances, stations)
