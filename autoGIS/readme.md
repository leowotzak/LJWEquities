
# autoGIS: a demographic lookup utility

## What is it?

autoGIS is a python command-line script that automates the plotting of addresses on a map and the extraction of demographic data in relation to those addresses. The script uses Esri ArcGIS API
to automatically geolocate lists of addresses. Then, the demographic data from the area immediately surrounding (1-mile) the address is pulled. Together, the addresses and demographic data are plotted on an interactive map

## How to Use

Using the script is quite easy, to pull data for a single worksheet, use the command below

`python main.py excel_worksheet`

Multiple inputs are also supported

`python main.py excel_worksheet excel_worksheet ...`

## How to install

Simply navigate to the project directory and execute the following command:

`python setup.py install`

## Dependencies

- arcgis
- pandas

## license

(link to license)