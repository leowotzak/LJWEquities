#!/usr/bin/env python

import argparse
import logging
import os

import pandas as pd
from arcgis.geocoding import batch_geocode, geocode, get_geocoders
from arcgis.geoenrichment import enrich
from arcgis.gis import GIS
from dotenv import load_dotenv

logging.basicConfig(filename="main.log", encoding="utf-8", level=logging.INFO)

# * Create input for excel sheet
parser = argparse.ArgumentParser(
    description="Geocode excel workbook addresses")

parser.add_argument(
    "workbook",
    type=str,
    nargs=1,
    help="The excel workbook that needs to be geocoded",
)

if __name__ == "__main__":

    load_dotenv()
    workbook = parser.parse_args().workbook[0]
    logging.info(f"Using workbook: {workbook}")

    # * Geocoding require arcGIS credentials and a login
    USER, PASS = os.environ.get("USERNAME"), os.environ.get("PASSWORD")
    my_gis = GIS("http://www.arcgis.com", username=USER, password=PASS)
    geocoder = get_geocoders(my_gis)[0]

    logging.info(
        f"Signed into ArcGIS w/ username: {USER} and password: {PASS}")

    addresses = pd.read_excel(workbook,
                              index_col=0,
                              squeeze=True,
                              dtype="string")["Full Address"]
    addresses_demographics = addresses.apply(lambda row: enrich([row]).squeeze())

    output_df = pd.concat([addresses, addresses_demographics], axis=1)
    with pd.ExcelWriter("demographic_data.xlsx") as writer:
        demographic_data_df.to_excel(writer)
