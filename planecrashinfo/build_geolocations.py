#! /usr/bin/env python

"""
Build a JSON file with geo-locations from plane crash places in the DB.
"""

import os
import time
import json
import random

import geopy
from geopy.geocoders import Nominatim
import pandas as pd

from planecrashinfo_light import clean_database


geolocator = Nominatim()


def location_to_latlon(place):
    """
    Get lat/lon dict or None for some place.
    """
    try:
        # Can raise geopy.exc.GeocoderServiceError,
        # so be gentle and give it some time to breathe.
        location = geolocator.geocode(place)
        time.sleep(random.random())
    except: # geopy.exc.GeocoderTimedOut:
        print('* ' + place, None)
        return None
    if location is None:
        print('* ' + place, None)
        return None
    print(place, (location.latitude, location.longitude))
    return {'lat': location.latitude, 'lon': location.longitude}


def get_geolocations(df, previous=None):
    """
    Return a dict with lat/lon for origins and destinations of one df."

        {
            'Bergen': {'lat': 60.3943532, 'lon': 5.325551},
            'Cairo': {'lat': 30.0488185, 'lon': 31.2436663},
            'Moroni Hahaya': None,
            ...
        }
    """
    res = previous or {}
    for name in ['Origin', 'Destination']:
        s = df.groupby(name).size().sort_values(ascending=True)
        for loc, count in s.items():
            # ignore unspecific place
            if loc in ('Sightseeing', 'Training', 'Test flight', 'Military exercises', 'aerial survelliance'):
                print('* Ignoring: %s' % loc)
                continue
            # ignore known place
            if res.get(loc, None) != None:
                print('* Already found: %s' % loc)
            else:
                latlon = location_to_latlon(loc)
                res[loc] = latlon
    return res


def build():
    """
    Build a file with gelocations for places in the database.
    """
    geolocs = {}
    geolocs_path = 'data/geolocs.json'
    if os.path.exists(geolocs_path):
        geolocs = json.load(open())
    print('Starting with %d' % len(geolocs))

    for y in range(1921, 2017):
        path = 'data/%d_original.csv' % y
        print('Loading %s' % path)
        df = pd.read_csv(path)
        df = clean_database(df)
        geolocs.update(get_geolocations(df, geolocs))
        json.dump(geolocs, open(path, 'w'), indent=4)
        print('Saved %d to %s\n' % (len(geolocs), geolocs_path))


if __name__ == '__main__':
    build()
