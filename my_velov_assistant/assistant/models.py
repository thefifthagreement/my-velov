import json
import os
import urllib.request

from django.db import models

from my_velov_assistant.users.models import User

DECAUX_API_KEY = os.environ["DECAUX_API_KEY"]
DECAUX_API_URL = "https://api.jcdecaux.com/vls/v3/stations"


def get_stations(city: str = "lyon") -> list:
    """Returns the list of the velov stations filtered by the city."""

    url = f"{DECAUX_API_URL}?apiKey={DECAUX_API_KEY}"
    response = urllib.request.urlopen(url)
    stations = json.loads(response.read().decode())

    # filtering using the city parameter
    return [s for s in stations if s["contractName"] == city]


class ApiCall(models.Model):
    """Log the call to the Google Direction API"""

    api_name = models.CharField(max_length=20, null=False, default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    called_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.api_name} api called at {self.called_at:%H:%M %Y-%m-%d} by {self.created_by}"
