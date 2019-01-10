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


def get_disruptions(client, prefs):
    '''
    Fetch the disruptions near the user from the database

    Parameters: client (sodapy.Socrata() object) - database client
                prefs (UserPreferences() object) - user preferences

    ---

    Information needed for query
    1) Starting and finishing date (compare to current date)
    2) Location (compare to current_location +- max_distance)

    SQL:    SELECT * FROM table
            WHERE starting_date <= current_date <= finishing_date 
            AND   haversine(current_location, location) <= max_distance

    Current implementation: Large query, then filter data
    Target implementation: Specific query, little to no filtering
    '''

    # Get rows
    result_set = client.get(detour.IDENTIFIER,
                            select="starting_date, finish_date, status, description")

    # Filter out the disruptions that aren't currently active
    active_results = list(filter(between_date, result_set))

    # Filter out the disruptions that are outside of the maximum distance
    relative_results = list(filter(within_distance, [active_results, prefs]))

    # Display our findings
    [print(r, end="\n\n") for r in relative_results]
    print("{} of {}".format(type(relative_results), type(relative_results[0])))
    input("Enter any key to continue")


def set_preferences(prefs, option):
    '''
    Function that allows the user to change the <option> option of the <prefs> user preference object

    Parameters: prefs (UserPreferences() object) - user preferences
                option (String) - preference item to change
    '''

    if option == "distance":
        print("SET DISTANCE\n", prefs)
        prefs.set_distance(input("Enter a max distance: "))

    elif option == "manual_location":
        print("SET MANUAL\n", prefs)
        prefs.set_manual_location(input("Enter 'true' for manual distance, 'false' for automatic distance: "))

    elif option == "coordinates":
        print("SET COORDINATES\n", prefs)
        if prefs.get_manual_location():
            new_lat = float(input("Enter latitude: "))
            new_lon = float(input("Enter longitude: "))
            prefs.set_location(new_lat, new_lon)
        else:
            prefs.set_location()


def report_issue():
    '''
    Displays information that the user could use to report issues with this program
    '''

    print("To report an issue, post with all related artifacts (error codes, steps to replicate, machine specs) at\n\thttps://github.com/ttamre/detour/issues\n")
    print("To contact the developer, send an email to the following address with 'Detour Project' in the subject line\n\tttamre@ualberta.ca\n")
    input("Enter any key to continue")


def between_date(results):
    '''
    Helper function that returns true if the current date is in between a result's starting and finish date, false otherwise

    Parameter: results (Dictionary) - result of a query
    Return: true or false
    '''

    start_date   = results["starting_date"]
    finish_date  = results["finish_date"]
    current_date = datetime.datetime.now().isoformat()
    return start_date <= current_date <= finish_date


def within_distance(args):
    '''
    Helper function that returns true if the disruption's location is within <prefs.get_distance()> km away of the user

    Parameter: args (list) - results, prefs
                - results (Dictionary) - results of a query
                - prefs (UserPreferences() object) - user preferences
    Return: true or false
    '''
    results, prefs = args

    disruption_coordinates = results["location"]
    target = set(disruption_coordinates)

    current_location = prefs.get_coordinates()
    curr = current_location.to_set()

    distance = haversine.haversine(target, curr)
    max_distance = prefs.get_distance()
    return distance <= max_distance