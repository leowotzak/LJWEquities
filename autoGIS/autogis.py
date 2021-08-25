#!/usr/bin/env python

import argparse
import logging
import os
from pathlib import Path

import pandas as pd
from arcgis.geocoding import batch_geocode, geocode, get_geocoders
from arcgis.geoenrichment import enrich
from arcgis.gis import GIS
from dotenv import load_dotenv

logging.basicConfig(filename="autogis.log", encoding="utf-8", level=logging.INFO)

# * Create input for excel sheet

def dir_path(string):
    """Type for use as CLI verification"""
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

parser = argparse.ArgumentParser(
    description="Geocode excel workbook addresses")

parser.add_argument(
    "workbook",
    type=argparse.FileType('r', encoding='utf-8'),
    nargs='+',
    help="The excel workbook that needs to be geocoded",
)

parser.add_argument(
    "-output",
    default=str(Path.home()),
    nargs='?', 
    type=dir_path,
    help="The output path for the output dataframe"
)

def enrich_workbook(file, filepath) -> None: 
    """Demographics are retrieved then the two dataframes are stitched together"""
    addresses = pd.read_excel(file,
                              index_col=0,
                              squeeze=True,
                              dtype="string")["Full Address"]
    addresses_demographics = addresses.apply(lambda row: enrich([row]).squeeze())
    output_df = pd.concat([addresses, addresses_demographics], axis=1)

    with pd.ExcelWriter(filepath+f"File_{str(output_files_count)}.xlsx") as writer:
        demographic_data_df.to_excel(writer)

    output_files_count += 1

if __name__ == "__main__":

    load_dotenv()
    output_files_count = 1
    workbooks = parser.parse_args().workbook
    output_dir = parser.parse_args().output

    # Geocoding require arcGIS credentials and a login
    USER, PASS = os.environ.get("USERNAME"), os.environ.get("PASSWORD")
    my_gis = GIS("http://www.arcgis.com", username=USER, password=PASS)
    geocoder = get_geocoders(my_gis)[0]
    logging.info(
        f"Signed into ArcGIS w/ username: {USER} and password: {PASS}")

    for workbook in workbooks:
        enrich_workbook(workbook, output_dir)
