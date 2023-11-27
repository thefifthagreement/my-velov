My velo'v assistant
==================

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

Where is the nearest bike available from my location and is there a free place near my destination ?

This app aims to answer these questions. The first version was available on Heroku.

:License: MIT

Description
===========

Velo'v is a bike rental service here in Lyon (FR). Using the geolocation the app search for the nearest bike available.

Then if a destination address is given, the app search for the nearest station to the destination location with a free place.

Assistant app
-------------

The ``station`` library define the velo'v station dataclass. The function `get_stations` uses the JCDECAUX API to retrieve the bike stations.

The ``point`` library contains the function using the Google Geocode API to extract the coordinates from the destination address.

The maps are created using ``folium``.

