#!/usr/bin/env python3

"""
File:           options.py
Descrtiption:   Functionality for menu options in detour.py

Author:     Tem Tamre
Contact:    ttamre@ualberta.ca
Version:    1.0
"""

import sodapy
import datetime
import haversine
import detour

def get_disruptions(client, pref):
    '''
    Information needed for query
    1) Starting and finishing date (compare to current date)
    2) Location (compare to current_location +- max_distance)

    SQL:    SELECT * FROM table
            WHERE starting_date <= current_date <= finishing_date 
            AND   haversine(current_location, location) <= max_distance

    SoQL:   ?$where tarting_date <= current_date <= finishing_date
    '''
    current_date = datetime.datetime.now().isoformat()
    current_location = pref.get_coordinates()
    max_distance = pref.get_distance()

    url = detour.SODA_URL + "/resource/" + detour.RESOURCE + ".json?$query="
    statement = "SELECT * WHERE starting_date <= {current_date} <= finishing_date".format(current_date=current_date)
    query = url + statement

    result_set = client.get(detour.RESOURCE, query=query)
    print(result_set)


def set_preferences(pref, option):
    if option == "distance":
        print("SET DISTANCE\n", pref)
        pref.set_distance(input("Enter a max distance: "))

    elif option == "manual_location":
        print("SET MANUAL\n", pref)
        pref.set_manual_location(input("Enter 'true' for manual distance, 'false' for automatic distance: "))

    elif option == "coordinates":
        print("SET COORDINATES\n", pref)
        if pref.get_manual_location():
            new_lat = float(input("Enter latitude: "))
            new_lon = float(input("Enter longitude: "))
            pref.set_location(new_lat, new_lon)
        else:
            pref.set_location()