#!/usr/bin/env python3

"""
Detour
Traffic disruption locator for the city of Edmonton
    Copyright (C) 2019 Tem Tamre

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

File:           preferences.py
Descrtiption:   User preferences object

Author:     Tem Tamre
Contact:    ttamre@ualberta.ca
Version:    1.0
"""

import requests

LOCATION = "http://ipinfo.io/loc"

class DistanceError(Exception): pass
class CoordinateError(Exception): pass

class UserPreferences():
    def __init__(self):
        self.distance = 10.0                # Distance (km) to search around the user for distruptions
        self.manual_location = False        # True for location services, false for manual coordinate entry
        self.coordinates = Coordinate()     # Current location

        # Initialize our empty coordinate
        self.set_location()


    def get_distance(self):
        return self.distance

    def get_manual_location(self):
        return self.manual_location

    def get_coordinates(self):
        return self.coordinates

    
    def set_distance(self, new_distance):
        new_distance = float(new_distance)
        if new_distance >= 0:
            self.distance = new_distance
        else:
            raise DistanceError

    def set_manual_location(self, manual):
        manual = manual[0].lower()
        if manual in "ty1":     # True, Yes, 1
            self.manual_location = True
        if manual in "fn0":     # False, No, 0
            self.manual_location = False

    def set_location(self, new_lat=None, new_lon=None):
        if self.manual_location:
            # Take the user's manual inputs
            self.coordinates.set_lat(new_lat)
            self.coordinates.set_lon(new_lon)
        else:
            # Get user's approximate GPS coordinates
            self._update_location()

    def _update_location(self):
        req = requests.get(LOCATION)
        text = req.text
        coords = text.rstrip().split(",")

        self.coordinates.set_lat(float(coords[0]))
        self.coordinates.set_lon(float(coords[1]))

    def __str__(self):
        return "Distance: {}km\nManual Location: {}\nCoordinates: {}".format(self.distance, self.manual_location, self.coordinates)


class Coordinate():
    def __init__(self, lat=None, lon=None):
        self.lat = lat      # Latitude  (+90 to -90)
        self.lon = lon      # Longitude (+180 to -180)
    
    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def set_lat(self, new_lat):
        if (-90 <= new_lat <= 90):
            self.lat = new_lat
        else:
            raise CoordinateError

    def set_lon(self, new_lon):
        if (-180 <= new_lon <= 190):
            self.lon = new_lon
        else:
            raise CoordinateError

    def to_set(self):
        return {self.lat, self.lon}

    def __str__(self):
        return "{},{}".format(self.lat, self.lon)