#!/usr/bin/env python

import os
import argparse
import pandas as pd

from arcgis.gis import GIS
from arcgis.geocoding import get_geocoders, batch_geocode, geocode
from arcgis.geoenrichment import enrich

# * Logging
import logging
logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)

if __name__ == "__main__":

