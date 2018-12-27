#!/usr/bin/env python3

"""
File:           detour.py
Descrtiption:   Python application that displays real-time traffic disruptions
                using the city of Edmonton open data portal

Author:     Tem Tamre
Contact:    ttamre@ualberta.ca
Version:    1.0

TODO
    Option 1 - Not complete
    Option 2 - Not started
    Option 3 - Complete

    Documentation - Not complete
    Testing - Not complete
"""

import sodapy
from consolemenu import *
from consolemenu.items import *
import options
import preferences

SODA_URL = "data.edmonton.ca"
RESOURCE = "ju4q-wijd"
PREFERENCES = preferences.UserPreferences()


def main():
    # Create our client and address
    client = sodapy.Socrata(SODA_URL, None)

    # Create our menu objects
    main_menu = ConsoleMenu("DETOUR: Real-time traffic distruption data", "Current location: {}".format(PREFERENCES.get_coordinates()))
    preferences_menu = ConsoleMenu("Preferences", "Set your application preferences")

    # Add menu options to our ConsoleMenu object
    get_disruptions = FunctionItem("Get traffic distruptions near your position", options.get_disruptions, [PREFERENCES])
    
    set_preferences = SubmenuItem("Set your application preferences", preferences_menu)
    set_preferences_distance = FunctionItem("Set maximum distance (0 for no maximum)", options.set_preferences, [PREFERENCES, "distance"])
    set_preferences_manual_location = FunctionItem("Turn on/off manual location", options.set_preferences, [PREFERENCES, "manual_location"])
    set_preferences_coordinates = FunctionItem("Set coordinates (if manual coords are on)", options.set_preferences, [PREFERENCES, "coordinates"])

    main_menu.append_item(get_disruptions)
    main_menu.append_item(set_preferences)
    preferences_menu.append_item(set_preferences_distance)
    preferences_menu.append_item(set_preferences_manual_location)
    preferences_menu.append_item(set_preferences_coordinates)

    main_menu.show()


if __name__ == "__main__":
    main()