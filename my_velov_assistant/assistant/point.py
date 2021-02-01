"""Dataclass and functions to manipulate coordinates (lat, lon)"""
import json
import os
import urllib.request
from dataclasses import astuple, dataclass
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


def get_distance(pointA: Point, pointB: Point) -> float:
    """Compute the distance between two points coordinates (lat, lon)
    using the Haversine formula

    :param point1: The first point
    :param point2: The second point
    :return: The distance between the points using the Haversine formula
    """

    pointA = astuple(pointA)
    pointB = astuple(pointB)
    return haversine(pointA, pointB)


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


def get_centered_location(pointA: Point, pointB: Point) -> Point:
    """Compute and returns the center between PointA and Point

    :param pointA: The current location
    :param pointB: The destination
    :return: The centered location between point A and point B
    """

    centered_latitude = (pointA.latitude + pointB.latitude) / 2
    centered_longitude = (pointA.longitude + pointB.longitude) / 2

    return Point(centered_latitude, centered_longitude)
