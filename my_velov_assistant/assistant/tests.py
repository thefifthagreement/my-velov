from django.test import TestCase

from my_velov_assistant.users.tests.factories import UserFactory

from .models import ApiCall
from .point import Point, get_distance
from .stations import (
    Station,
    Stations,
    get_nearest_free_bike,
    get_nearest_free_place,
    get_stations,
)


# ApiCall
class ApiCallTestCase(TestCase):
    def test_new_call_is_registered(self):
        api_call_count = ApiCall.objects.count()
        # create a fake user
        user = UserFactory()
        ApiCall.objects.create(created_by=user)
        self.assertEqual(ApiCall.objects.count(), api_call_count + 1)

    def test_new_call_api_name(self):
        # create a fake user
        user = UserFactory()
        api_call = ApiCall.objects.create(api_name="test_api", created_by=user)
        self.assertEqual(api_call.api_name, "test_api")


# Velov test cases
class VelovTestCase(TestCase):
    def test_get_station_is_not_empty(self):
        # check that the decaux api setup is correct
        velov_stations = get_stations()
        self.assertNotEquals(len(velov_stations), 0)


# Distances
class DistanceTestCase(TestCase):
    def setUp(self) -> None:
        self.lyon = Point(45.7597, 4.8422)
        self.paris = Point(48.8567, 2.3505)
        self.station1 = Station(
            number=1,
            name="museum",
            position=Point(45.774526, 4.848443),
            free_bike=10,
            free_place=0,
        )
        self.station2 = Station(
            number=2,
            name="cité",
            position=Point(45.784812, 4.856432),
            free_bike=0,
            free_place=20,
        )
        self.station3 = Station(
            number=3,
            name="porte",
            position=Point(45.777521, 4.844922),
            free_bike=1,
            free_place=20,
        )
        self.stations: Stations = [self.station1, self.station2, self.station3]

    def test_distance_lyon_paris(self):
        self.assertAlmostEqual(get_distance(self.lyon, self.paris), 392.22, delta=0.1)

    def test_nearest_free_bike(self):
        nearest = get_nearest_free_bike(Point(45.7730961, 4.8418148), self.stations)
        self.assertEquals(nearest.number, 1)

    def test_nearest_free_place(self):
        nearest = get_nearest_free_place(Point(45.7730961, 4.8418148), self.stations)
        self.assertEquals(nearest.number, 3)

    # destination format
