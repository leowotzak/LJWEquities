
# autoGIS: a demographic lookup utility

## What is it?

---

autoGIS is a python command-line script that automates the plotting of addresses on a map and the extraction of demographic data in relation to those addresses. The script uses Esri ArcGIS API
to automatically geolocate lists of addresses. Then, the demographic data from the area immediately surrounding (1-mile) the address is pulled. Together, the addresses and demographic data are plotted on an interactive map

<br>

## How to Use

---

Using the script is quite easy, to pull data for a single worksheet, use the command below

`autogis excel_worksheet`

Multiple inputs are also supported

`autogis excel_worksheet excel_worksheet ...`

<br>

## How to install

---

## MacOS / Linux

<br>

Simply navigate to the project directory and execute the following command:

`python setup.py install`

Then, make sure that the script is executable by executing the following:

`sudo chmod +x autogis`

Then, copy the script to:

`/usr/local/bin`

The script should now be executable from anywhere!

<br>

## Windows

<br>

Run the following on the command line:

`setx path "%path%;C:\path\to\autogis.py"`

The script should now be executable from anywhere!

<br>

## Dependencies

---

- arcgis
- pandas

<br>

## License

---

(link to license)