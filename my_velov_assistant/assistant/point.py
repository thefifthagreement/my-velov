from dataclasses import dataclass

from haversine import haversine


@dataclass
class Point:
    """Definition of a point with coordinates, latitude and longitude"""

    latitude: float
    longitude: float


def get_distance(point1: Point, point2: Point) -> float:
    """Returns the distance between two points (lat, lon)
    using the Haversine formula"""

    point1 = (point1.latitude, point1.longitude)
    point2 = (point2.latitude, point2.longitude)
    return haversine(point1, point2)
