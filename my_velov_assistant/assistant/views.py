from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from my_velov_assistant.assistant.point import Point
from my_velov_assistant.assistant.stations import get_nearest_free_bike, get_stations


@login_required
def index(request):
    # get the nearest station with a free bike
    if request.method == "POST":

        # the position of the user
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        position = Point(latitude=float(latitude), longitude=float(longitude))

        # read the stations
        stations = get_stations()
        nearest, distance = get_nearest_free_bike(position, stations)

        context = {
            "nearest_free_bike": nearest.name,
            "distance": round(distance, 2),
        }
        return render(request=request, context=context, template_name="pages/home.html")
    return render(request=request, template_name="pages/home.html")
