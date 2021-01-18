# image-processing - Scraping, image processing, and data analysis for IXP plots

Includes functions for scraping images from IXP stats pages and extracting time-series traffic volume data from retrieved images. Traffic volume information can be interpreted using included synthetic control and changepoint detection functionality. 

For Python 3.7+.

Dependencies:
numpy, matplotlib, os, datetime, pandas, ruptures, collections, PIL, dateutil, pytesseract, tslib

You will need to install Tesseract OCR. If using Windows, you can use the executable here: https://github.com/UB-Mannheim/tesseract/wiki. The default path in the plot_image_processing script is C:\Program Files\Tesseract-OCR\tesseract.exe.

You will also need tslib, which is found here: https://github.com/jehangiramjad/tslib. Place the tslib folder in the same folder that the scripts are located in. The file's name should be tslib; if it is tslib-master, rename to tslib.

# Documentation

Example usage included at the bottom of each file.

plot_image_processing: Includes functions for determining the color used to plot y-values in the input IXP plot image, using optical character recognition to determine the values on the x and y axes, and scaling the pixels of the selected color to the values on the x and y axes to obtain time-series data.

data_stitching: Includes functions for interpreting the data obtained from plot_image_processing, passing the obtained x and y-values to a dictionary with data from multiple dates for further processing, and appending data from multiple dates for a single IXP to a single list, which is then added to a dictionary of multiple IXPs.

synth_control_and_interpolation: Includes functions for preparing data to be used by the synthetic control package tslib. Creates dataframes for before and after the selected intervention date and processes datasets with different sampling frequencies.


