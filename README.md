# Live2D-CSV-Converter
Changes ID field to match Name field within Live2D ID constraints

## Still to Come...
An exe release that allows drag and drop conversion

A fork thats has a minimal GUI for adding and naming output file

A requirements.txt for python environment setup

## Requirements
This program is dependent on:

pandas for dataframe
`pip install pandas`

## Usage
The program takes one argument, the path to the CSV you want to convert

The output file will be named `corrected.csv` 


Example

`python live2d_CSV_cleaner.py 'path_to_your.csv'`

Ensure proper escaping and formatting in the path of course!

In the future there will be a second argument for output file name

e.g `python live2d_CSV_cleaner.py 'path_to_your.csv' 'name_of_corrected.csv'`

