"""Dataclass and functions to manipulate coordinates (lat, lon)"""
from dataclasses import dataclass

from haversine import haversine


@dataclass
class Point:
    """Definition of a point with latitude and longitude coordinates"""

    #: the latitude of the point
    latitude: float
    #: the longitude of the point
    longitude: float


def get_distance(point1: Point, point2: Point) -> float:
    """Returns the distance between two points coordinates (lat, lon)
    using the Haversine formula

    :param point1: The first point
    :param point2: The second point
    :return: The distance between the points using the Haversine formula
    """

    point1 = (point1.latitude, point1.longitude)
    point2 = (point2.latitude, point2.longitude)
    return haversine(point1, point2)
