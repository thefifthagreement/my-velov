from dataclasses import astuple

import folium
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from my_velov_assistant.assistant.point import (
    Point,
    get_centered_location,
    get_coordinates,
)
from my_velov_assistant.assistant.stations import (
    get_nearest_free_bike,
    get_nearest_free_place,
    get_stations,
)


@login_required
def index(request):
    context = {"search": False}
    # get the nearest station with a free bike
    if request.method == "POST":

        # the location of the user
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        location = Point(latitude=float(latitude), longitude=float(longitude))

        # read the stations
        stations = get_stations(request.user)

        nearest, distance = get_nearest_free_bike(location, stations)

        # get the center between current locatio and destination
        latitude, longitude = get_centered_location(location, nearest.location)

        m = folium.Map(
            width=300, height=300, location=(latitude, longitude), zoom_start=20
        )
        folium.Marker(
            [latitude, longitude], tooltip="Your location", icon=folium.Icon()
        ).add_to(m)

        folium.Marker(
            [nearest.location.latitude, nearest.location.longitude],
            tooltip="Nearest free bike",
            icon=folium.Icon(color="purple"),
        ).add_to(m)

        context = {
            "search": True,
            "nearest_station": nearest,
            "distance": round(distance, 2),
            "map": m._repr_html_(),
        }
    return render(request=request, context=context, template_name="pages/home.html")


@login_required
def destination(request):
    if request.method == "POST":
        destination_address = request.POST.get("destination")
        destination_location = get_coordinates(destination_address, request.user)
        latitude, longitude = astuple(destination_location)

        # read the stations
        stations = get_stations(request.user)

        nearest, distance = get_nearest_free_place(destination_location, stations)

        # get the center between current locatio and destination
        latitude, longitude = get_centered_location(
            destination_location, nearest.location
        )

        m = folium.Map(
            width=300, height=300, location=(latitude, longitude), zoom_start=20
        )
        folium.Marker(
            [destination_location.latitude, destination_location.longitude],
            tooltip="Your destination",
            icon=folium.Icon(),
        ).add_to(m)

        folium.Marker(
            [nearest.location.latitude, nearest.location.longitude],
            tooltip="Nearest free place",
            icon=folium.Icon(color="purple"),
        ).add_to(m)

        context = {
            "nearest_station": nearest,
            "distance": round(distance, 2),
            "map": m._repr_html_(),
        }
        return render(
            request=request, context=context, template_name="pages/destination.html"
        )
    return render(request=request, template_name="pages/home.html")
