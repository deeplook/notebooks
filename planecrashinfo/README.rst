Plane Crash Info
================

This is an exploration of data found at http://planecrashinfo.com.

The real code and the downloaded data will follow, soon...

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
