# Live2D-CSV-Converter
Never again wonder what the hell ArtMesh156 is when setting up clipping masks or setting up model lighting!

Updates the ArtMesh ID field to match the ArtMesh Name field within the ArtMesh ID fields naming constraints.

Live2D IDs can only have alpanumeric characters and underscores.

## Still to Come...
A fork thats has a minimal GUI for adding and naming output file

A requirements.txt for python environment setup

### PLEASE NOTE
You need to have you Live2D project open during the export from Live2D and during the conversion process, then import the `corrected.csv` back into Live2D.

To export or import the CSV file, in Live2D navigate to the top menu and go to Modeling>Bulk setting of model objects>Export/Import

This is a Live2D constraint on how they handle the GUIDs, if the project is closed and then you try to import, the import will fail, because the GUIDs will be different. Unfortunately this cant be worked around as there is no way to "know" what the new GUIDs will be. 

Of course after the import is completed, the Live2D project can be closed an reopened as normal. Think of the GUIDs as relating to an instance of Live2D.

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

## Testimonials
"I love it! The programmer who made this is so hot and smart!" - Cillia

"Cool" - Python Projects 007 (comment on Twitter)
