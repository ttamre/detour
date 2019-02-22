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

    
File:           detour.py
Descrtiption:   Python application that displays real-time traffic disruptions
                using the city of Edmonton open data portal

Data portal: https://data.edmonton.ca/Transportation/Traffic-Disruptions-Map-View/87ck-293k

Author:     Tem Tamre
Contact:    ttamre@ualberta.ca
Version:    1.0

TODO
    Option 1 - Not complete
    Option 2 - Complete
    Option 3 - Rethink

    Documentation - Not complete
    Testing - Not complete
"""

import sodapy
from consolemenu import ConsoleMenu
from consolemenu.items import FunctionItem, SubmenuItem
import options
import preferences

SODA_URL    = "data.edmonton.ca"
IDENTIFIER  = "ju4q-wijd"
API_KEY     = None
PREFERENCES = preferences.UserPreferences()


def main():
    '''
    Create database client and menu, then wait for user input and execute the associated functions
    '''

    # Create our client and address
    client = sodapy.Socrata(SODA_URL, API_KEY)

    # Create our menu objects
    main_menu = ConsoleMenu("DETOUR: Real-time traffic distruption data", "Current location: {}".format(PREFERENCES.get_coordinates()))
    preferences_menu = ConsoleMenu("Preferences", "Set your application preferences")

    # Add menu options to our ConsoleMenu object
    get_disruptions = FunctionItem("Get traffic distruptions near your position", options.get_disruptions, [client, PREFERENCES])
    
    set_preferences = SubmenuItem("Set your application preferences", preferences_menu)
    set_preferences_distance = FunctionItem("Set maximum distance (0 for no maximum)", options.set_preferences, [PREFERENCES, "distance"])
    set_preferences_manual_location = FunctionItem("Turn on/off manual location", options.set_preferences, [PREFERENCES, "manual_location"])
    set_preferences_coordinates = FunctionItem("Set coordinates (if manual coords are on)", options.set_preferences, [PREFERENCES, "coordinates"])

    report_issue = FunctionItem("Report an issue or contact the developer", options.report_issue)

    # Entering the number displayed by each menu option will execute the function linked to that menu item
    main_menu.append_item(get_disruptions)
    main_menu.append_item(set_preferences)
    main_menu.append_item(report_issue)
    preferences_menu.append_item(set_preferences_distance)
    preferences_menu.append_item(set_preferences_manual_location)
    preferences_menu.append_item(set_preferences_coordinates)

    main_menu.show()


if __name__ == "__main__":
    main()