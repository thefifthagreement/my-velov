import json
import os
import urllib.request

from django.db import models

from my_velov_assistant.users.models import User

API_KEY = os.environ["API_KEY"]
API_URL = "https://api.jcdecaux.com/vls/v3/stations"


def get_stations(city: str = "lyon") -> list:
    """Returns the list of the velov stations filtered by the city."""

    url = f"{API_URL}?apiKey={API_KEY}"
    response = urllib.request.urlopen(url)
    stations = json.loads(response.read().decode())

    # filtering using the city parameter
    return [s for s in stations if s["contractName"] == city]


class ApiCall(models.Model):
    """Log the call to the Google Direction API"""

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    called_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Called at {self.called_at:%H:%M %Y-%m-%d} by {self.created_by}"
