#! /usr/bin/env python

"""
Initial code for working with data from PlaneCrashInfo.com.

More to come...
"""

import re

import numpy as np
import pandas as pd


# database cleaning

US_STATES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District Of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
]

US_STATES_FLAT = [entry[0] for entry in US_STATES] + [entry[1] for entry in US_STATES]

def country_of_loc(location):
    """
    Get country of given location.

    E.g. 'St. Moritz, Switzerland' -> 'Switzerland' or
    'Jackson, Mississippi' -> 'USA'
    """
    if type(location) != str:
        return '?'
    country = location.split(',')[-1].strip()
    if country in US_STATES_FLAT:
        country = 'USA'
    return country


def int_or_nan(x):
    try:
        x = int(x)
    except ValueError:
        x = np.nan
    return x


def split_fatalities(entry):
    """
    Split 'Fatalities' entry into dictionary.

    '?' are converted to np.nan. Counts should be ints, not floats...

    E.g. '15 (passengers:13 crew:2)' 
      -> {'total':15, 'passengers':13, 'crew':2}.
    """
    names = 'total passengers crew'.split()
    counts = re.findall('(\?|\d+)', entry)
    counts = [int_or_nan(c) for c in counts]
    return dict(list(zip(names, counts)))


def clean_database(df):
    "Return copy of database after cleaning."

    dfc = df.copy()

    # drop useless columns
    dfc = dfc.drop(['Registration:', 'Flight #:', 'cn / ln:'], axis=1)

    # remove trailing ':' in index/column names
    dfc = dfc.rename(columns={cn: cn[:-1] for cn in list(dfc.columns)})

    # replace all '?' values with NaN
    dfc.replace(to_replace='?', value=np.nan, inplace=True)

    # make datetimeindex from date/time fields
    # dfc = dfc.set_index(dfc['Date'])
    dfc = dfc.set_index(pd.DatetimeIndex(dfc['Date']))
    dfc.sort_index(inplace=True)
    dfc = dfc.drop(['Date'], axis=1)

    # split route field into origin/destination
    values = dfc.Route.values
    dfc['Origin'] = [v.split(' - ')[0] if type(v) != float else np.nan for v in values]
    dfc['Destination'] = [v.split(' - ')[-1] if type(v) != float else np.nan for v in values]

    # split fatalities field
    dfc['Fatalities total'] = dfc['Fatalities'].apply(lambda x: split_fatalities(x)['total'])

    # make Ground field numeric (or nan)
    dfc['Ground'] = dfc['Ground'].apply(pd.to_numeric)

    # add country field extracted from accident location
    dfc['Location Country'] = dfc['Location'].apply(lambda x: country_of_loc(x))

    return dfc
