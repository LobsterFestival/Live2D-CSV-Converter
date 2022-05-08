# Live2D-CSV-Converter
Changes ID field to match Name field within Live2D ID constraints

## Still to Come...
A fork thats has a minimal GUI for adding and naming output file

A requirements.txt for python environment setup

### PLEASE NOTE
You need to have you Live2D project open during the export from Live2D and during the conversion process, then import the `corrected.csv` back into Live2D.

To export or import the CSV file, in Live2D navigate to the top menu and go to Modeling>Bulk setting of model objects>Export/Import

## Requirements
This program is dependent on:

pandas for dataframe structure
`pip install pandas`

## Usage
The program takes one argument, the path to the CSV you want to convert

The output file will be named `corrected.csv` 


Example

`python live2d_CSV_cleaner.py 'path_to_your.csv'`

Ensure proper escaping and formatting in the path of course!

In the future there will be a second argument for output file name

e.g `python live2d_CSV_cleaner.py 'path_to_your.csv' 'name_of_corrected.csv'`

