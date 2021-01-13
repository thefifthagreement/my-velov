import json
import os
import urllib.request

DECAUX_API_KEY = os.environ["DECAUX_API_KEY"]
DECAUX_API_URL = "https://api.jcdecaux.com/vls/v3/stations"


def get_stations(city: str = "lyon") -> list:
    """Returns the list of the velov stations filtered by the city."""

    url = f"{DECAUX_API_URL}?apiKey={DECAUX_API_KEY}"
    response = urllib.request.urlopen(url)
    stations = json.loads(response.read().decode())

    # filtering using the city parameter
    return [s for s in stations if s["contractName"] == city]
