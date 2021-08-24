#!/usr/bin/env python

import os
import argparse
import pandas as pd

from dotenv import load_dotenv
from arcgis.gis import GIS
from arcgis.geocoding import get_geocoders, batch_geocode, geocode
from arcgis.geoenrichment import enrich

# * CLI Interface
parser = argparse.ArgumentParser(description="Geocode excel workbook addresses")
parser.add_argument(
    "workbook",
    type=str,
    nargs=1,
    help="The excel workbook that needs to be geocoded",
)

# * Logging
import logging
logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)

if __name__ == "__main__":

    load_dotenv()

    workbook = parser.parse_args().workbook[0]
