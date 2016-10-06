#! /usr/bin/env python

"""
Get data from planecrashinfo.com and save it into a local CSV 'database'.
"""

import os
import re
import sys
import datetime

import numpy as np
import pandas as pd


def get_accident_years():
    """
    Get years with data from `planecrashinfo.com/database.htm`.

    Returns a list of integers, from 1920 to the current year,
    e.g. [1920, 1921, ..., 2016].
    """
    url = 'http://www.planecrashinfo.com/database.htm'
    dfs = pd.read_html(url, index_col=0)
    years = dfs[1].values.flatten()
    years = list(map(int, years[~np.isnan(years)]))
    return years


def get_accidents_per_year(year):
    """
    Get #crashes for given year like `planecrashinfo.com/2000/2000.htm`.

    Returns an integer representing the number of accidents for the given
    year (easy since there is no paging used planecrashinfo.com).
    """
    url = 'http://www.planecrashinfo.com/%d/%d.htm' % (year, year)
    dfs = pd.read_html(url)
    return len(dfs[0]) - 1


# not used yet
def get_single_accident_html(year, num):
    """
    Get data for some accident in some year like `planecrashinfo.com/2000/2000-14.htm`.
    """
    url = 'http://www.planecrashinfo.com/%d/%d-%d.htm' % (year, year, num)
    html = requests.get(url).text
    return html


def get_single_accident(year, num):
    """
    Get data for some accident in some year like `planecrashinfo.com/2000/2000-14.htm`.
    """
    url = 'http://www.planecrashinfo.com/%d/%d-%d.htm' % (year, year, num)
    dfs = pd.read_html(url, index_col=0, header=0)
    df = dfs[0]
    return df


# database handling

def get_database(years=[], verbose=True):
    "Get entire database, as one dataframe with all desired years."

    dfs = []
    for y in years or get_accident_years():
        for acc_num in range(1, get_accidents_per_year(y) + 1):
            # if acc_num > 4:
            #     break
            if verbose:
                print(y, acc_num)
            dfs.append(get_single_accident(y, acc_num))
    df_total = pd.DataFrame([df.T.iloc[0] for df in dfs])
    return df_total


def download_separate_years(years=[], verbose=True):
    "Scrape and store all data from `planecrashinfo.com` as single CSV files."

    # Best practice to avoid downloading identical files many times...

    for y in years:
        dest = 'data/%d_original.csv' % y
        if os.path.exists(dest):
            continue
        if verbose:
            print(y)
        try:
            df = get_database(years=[y], verbose=verbose)
        except TimeoutError:
            df = get_database(years=[y], verbose=verbose)
        df.to_csv(dest)


def build_one_database(years=[], verbose=True):
    "Build one database from separately downloaded files."

    dfs = []
    for y in years: # 1920 missing
        path = 'data/%d_original.csv' % y
        df = pd.read_csv(path)
        if verbose:
            print(y) 
        dfs.append(df)
    return pd.concat(dfs)


if __name__ == '__main__':
    download_separate_years(years=range(1921, 2017))
    # sys.exit(0)

    # df = get_database(years=range(1921, 2017), verbose=True)
    # path = 'data/1921-2016_original.csv'
    # df.to_csv(path)

    # build full database from single yearly files
    df_all = build_one_database(range(1921, 2017))
    path = 'data/data.csv'
    df_all.to_csv(path)
