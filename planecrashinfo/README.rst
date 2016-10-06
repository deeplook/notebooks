Plane Crash Info
================

This is an exploration of data found at http://planecrashinfo.com.

The real code and the downloaded data will follow, soon...

**N.B.** This is work in progress… If you have any suggestion, please feel free to raise an issue or provide a pull request.


Installation
------------

Conda ist the recommended packaging system, since pip cannot install ``basemap``. To install all dependencies, just run the following in your root environment::

  conda install basemap
  conda install pandas
  conda install jupyter
  pip install geopy

or set-up a new environment like this (should take < 30 secs)::

  conda create -n planes basemap pandas jupyter
  source activate planes
  pip install geopy
  ...
  # this is to remove the environment again:
  source deactivate
  conda env remove -n planes


Preparation
-----------

For the notebook to execute correctly it needs two data files, ``data.csv`` and ``geolocs.json`` which are checked into this repository, but can also be created by running the following, respectively::

  python build_database.py
  python build_geolocations.py

This might take quite a while, ca. 1-2 hours, and create a few additional CSV files, which are not needed for the notebook, but can be nice to play with.

