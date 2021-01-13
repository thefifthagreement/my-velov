from django.test import TestCase

from my_velov_assistant.users.tests.factories import UserFactory

from .models import ApiCall
from .point import Point, get_distance
from .stations import get_stations


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
    def test_distance_lyon_paris(self):
        lyon = Point(45.7597, 4.8422)
        paris = Point(48.8567, 2.3505)
        self.assertAlmostEqual(get_distance(lyon, paris), 392.22, delta=0.1)


# select nearest station with a free bike

# destination format

# select nearest free place from the destination
