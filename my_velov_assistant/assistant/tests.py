from django.test import TestCase

from my_velov_assistant.users.tests.factories import UserFactory

from .models import ApiCall


# ApiCall
class ApiCallTestCase(TestCase):
    def test_new_call_is_registered(self):
        api_call_count = ApiCall.objects.count()
        user = UserFactory()
        ApiCall.objects.create(created_by=user)
        self.assertEqual(ApiCall.objects.count(), api_call_count + 1)


# read the stations

# distance from position

# select nearest station with a free bike

# destination format

# select nearest free place from the destination
