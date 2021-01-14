"""Dataclass and functions to manipulate coordinates (lat, lon)"""
import json
import os
import urllib.request
from dataclasses import dataclass
from urllib.parse import urlencode

from haversine import haversine

from my_velov_assistant.assistant.models import ApiCall
from my_velov_assistant.users.admin import User

GEOCODE_API_URL = os.environ["GEOCODE_API_URL"]
GEOCODE_API_KEY = os.environ["GEOCODE_API_KEY"]


@dataclass
class Point:
    """Definition of a point with latitude and longitude coordinates"""

    #: the latitude of the point
    latitude: float
    #: the longitude of the point
    longitude: float


def get_distance(point1: Point, point2: Point) -> float:
    """Compute the distance between two points coordinates (lat, lon)
    using the Haversine formula

    :param point1: The first point
    :param point2: The second point
    :return: The distance between the points using the Haversine formula
    """

    point1 = (point1.latitude, point1.longitude)
    point2 = (point2.latitude, point2.longitude)
    return haversine(point1, point2)


def get_coordinates(address: str, user: User, city: str = "LYON, FR") -> Point:
    """Extract the latitude and longitude from address using Google Maps API

    :param adress: The adress to geocode
    :param user: The actual user
    :return: A Point
    """

    params = {"address": f"{address},{city}", "key": GEOCODE_API_KEY}
    url_params = urlencode(params)
    url = f"{GEOCODE_API_URL}?{url_params}"

    response = urllib.request.urlopen(url)

    # logging the call
    api_call = ApiCall.objects.create(api_name="GEOCODE", created_by=user)
    api_call.save()

    geocode = json.loads(response.read().decode())
    latlng = geocode["results"][0]["geometry"]["location"]

    return Point(latlng.get("lat"), latlng.get("lng"))
