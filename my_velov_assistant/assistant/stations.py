"""Dataclass and functions for the manipulation of the velov stations"""
import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Dict, List, Tuple

from my_velov_assistant.assistant.models import ApiCall
from my_velov_assistant.assistant.point import Point, get_distance
from my_velov_assistant.users.admin import User

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
    location: Point
    #: the number of free bikes
    free_bike: int
    #: the number of free places
    free_place: int


#: type alias for type hinting
Stations = List[Station]


def get_stations(user: User, city: str = "lyon") -> Stations:
    """Returns the list of the velov stations filtered by the city.

    :param: The actual user
    :param city: The city to filter the stations returned by the API
    :return: The list of station of the city
    """

    url = f"{DECAUX_API_URL}?apiKey={DECAUX_API_KEY}"
    response = urllib.request.urlopen(url)

    # logging the call
    api_call = ApiCall.objects.create(api_name="DECAUX", created_by=user)
    api_call.save()

    stations = json.loads(response.read().decode())

    # filtering using the city parameter
    return [
        Station(
            number=s["number"],
            name=s["name"],
            location=Point(s["position"]["latitude"], s["position"]["longitude"]),
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

    return next(filter(lambda s: s.number == number, stations), None)


def get_nearest_station(distances: Dict[int, float], stations: Stations):
    """Search of the nearest station using the distances

    :param distances: A dict of number -> distance
    :param stations: The list of velov stations
    :return: The nearest station and the distance in km
    """

    # the minimum of the distances
    nearest = min(distances.items(), key=lambda d: d[1])

    return (get_station(nearest[0], stations), nearest[1])


def get_nearest_free_bike(location: Point, stations: Stations) -> Tuple[Station, float]:
    """Search of the nearest station from the location with a free bike

    :param location: The user's location
    :param stations: The list of velov stations
    :return: The nearest station with a free bike and the distance in km
    """

    distances = {
        s.number: get_distance(location, s.location)
        for s in stations
        if s.free_bike > 0
    }
    return get_nearest_station(distances, stations)


def get_nearest_free_place(
    destination: Point, stations: Stations
) -> Tuple[Station, float]:
    """Search of the nearest station from the destination with a free place

    :param destination: The user's destination
    :param stations: The list of velov stations
    :return: The nearest station with a free place and the distance in km
    """

    distances = {
        s.number: get_distance(destination, s.location)
        for s in stations
        if s.free_place > 0
    }
    return get_nearest_station(distances, stations)
